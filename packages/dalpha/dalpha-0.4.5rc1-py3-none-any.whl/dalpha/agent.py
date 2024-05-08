import requests, json, boto3, io, sys, os
import time
import sentry_sdk
from requests.adapters import HTTPAdapter, Retry
from dataclasses import asdict

from dalpha.signal_handler import get_shutdown_requested
from dalpha.context import clear_context_evaluate, set_context, set_context_evaluate, get_context, Context
from dalpha.logging import logger
from dalpha.logging.events import Event

from dalpha.exception import BaseStatusCode


class Agent:
    def __get_internal_slack(self, header, api_id):
        try:
            response = requests.request("GET", os.path.join(self.base_url, f'inferences/{api_id}/owner'), headers=header)
            account = response.json()
            if account == -1:
                return "<!subteam^S05EP7HQ18V>"
            url = os.path.join(self.base_url, f'accounts/{account}/internal_slack')
            response = requests.request("GET", url, headers=header)
            return '<@'+ response.text + '>'
        except Exception as e:
            return 'error'

    # 1. constructor 로 넣어주는 경우
    # TODO(XXX): constructor 로 넣어주는 것은 production 코드에서는 지양해야 함.
    # ai-project-template 에서 production image build test code 에 넣어줄 것
    # 2. 환경변수로 넣어주는 경우
    # 3. .dalphacfg 로 넣어주는 경우

    # backend 에서 당겨오는 env
    # SQS 주소, Kafka 주소, service code 는 백엔드에서 받아옴
    # To-Be: 다른 AI 콜 해주는 Agent 의 token

    def __init__(
        self,
        api_id=int(os.environ.get('API_ID', 0)),
        use_sqs=bool(os.environ.get('USE_SQS', 'False') == 'True'),
        use_kafka=bool(os.environ.get('USE_KAFKA', 'False') == 'True'),
        dev_server=bool(os.environ.get('DEV_SERVER', 'True') == 'True'),
    ):
        if not isinstance(api_id, int): raise TypeError('api_id is not a int')
        if not isinstance(use_sqs, bool): raise TypeError('use_sqs is not a bool')
        if not isinstance(dev_server, bool): raise TypeError('dev_server is not a bool')
        if not isinstance(use_kafka, bool): raise TypeError('use_kafka is not a bool')

        self.token = os.environ['TOKEN']
        self.sentry_dsn = os.environ['SENTRY_DSN']
        self.max_retry = 5
        if dev_server:
            self.base_url = os.environ.get('DEV_BASE_URL', 'https://api.exp.dalpha.so')
            self.sentry_env = "exp"
        else:
            self.base_url = os.environ.get('BASE_URL', 'https://api.dalpha.so')
            self.sentry_env = "production"

        headers = {
        'token': self.token
        }
        print(self.base_url, self.sentry_env, dev_server)

        response = requests.request("GET", os.path.join(self.base_url,f"inferences/{api_id}"), headers = headers)
        if response.status_code != 200:
            logger.warning(f'error from get sqs url / response status_code {response.status_code}: {response.text}')
            self.service_code = None
        else:
            self.queue_url = response.json().get('sqs', None)
            self.kafka_topic = response.json().get('kafkaTopic', None)
            self.service_code = response.json().get('serviceCode', None)

        self.evaluate_url = os.path.join(self.base_url, f"inferences/{api_id}/evaluate")
        self.api_id = api_id
        self.mock = {}
        self.s3 = boto3.client('s3')

        # default
        self.use_kafka = False
        self.use_sqs = False

        if use_kafka:  # 우선순위 1. kafka
            from dalpha.kafka_cli import get_consumer

            if self.queue_url is None:
                logger.warning("kafka topic is not set")
                raise ValueError("kafka topic is not set")

            self.use_kafka = True
            self.kafka_consumer = get_consumer(self.kafka_topic, api_id)
        elif use_sqs:  # 우선순위 2. sqs (kafka가 없을 때만 사용)
            if self.queue_url is None and os.environ.get('QUEUE_URL',None) is None:
                logger.warning("sqs url is not set")
                raise ValueError("sqs url is not set")
            elif self.queue_url is None:
                self.queue_url = os.environ.get('QUEUE_URL',None)

            self.use_sqs = True
            self.sqs = boto3.client('sqs', region_name='ap-northeast-2')

        self.evaluates = {}
        self.poll_time = None

        set_context(Context(
            inference_id = api_id,
            service_code = self.service_code,
            env = "exp" if dev_server else "prod"
        ))
        sentry_sdk.set_context("context",asdict(get_context()))
        sentry_sdk.init(
            dsn=self.sentry_dsn,

            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0,
            environment = self.sentry_env
        )
        sentry_sdk.set_tag("api_id", api_id)
        sentry_sdk.set_tag("service_code", self.service_code)
        sentry_sdk.set_tag("engineer", self.__get_internal_slack(headers, api_id) )
        logger.info(
            message = "Dalpha agent initialized",
            event = Event.AGENT_INIT,
            data = {
                'inference_id': api_id,
                "use_sqs": self.use_sqs,
                "use_kafka": self.use_kafka,
                "dev_server": dev_server,
                "base_url": self.base_url,
                "queue_url": self.queue_url,
                "sentry_dsn": self.sentry_dsn,
            }
        )

    def set_mock(self, mock):
        self.mock = mock

    def batch(self, iterable, n):
        # Yield successive n-sized chunks from iterable.
        for i in range(0, len(iterable), n):
            yield iterable[i:i + n]
    
    '''
        message_id를 10개씩 끊어서 sqs에 batch delete 요청으로 메세지 삭제
    '''
    def delete_messages(self, message_ids):
        entries = list(map(lambda message_id: {
            'Id': str(message_id),
            'ReceiptHandle': self.evaluates[message_id]
        }, message_ids))
        for group in self.batch(entries, 10):
            try:
                self.sqs.delete_message_batch(
                    QueueUrl = self.queue_url,
                    Entries = group
                )
            except Exception as e:
                logger.error(f"Error while deleting messages\n{e}")
    
    '''
        evaluate이 유효한지 서버에 요청해서 유효하지 않은 메세지는 sqs에서 삭제
        유효한 메세지만 반환
    '''
    def filter_valid(self, messages):
        messages_to_delete = []
        messages_to_handle = []
        headers = {
            'token': self.token,
            'Content-Type': 'application/json'
        }
        for message in messages:
            endpoint = os.path.join(self.base_url, f"inferences/{self.api_id}/evaluate/id-poll/{message['id']}")
            with requests.Session() as s:
                # backoff time = backoff_factor * (2 ** (retry_number - 1)) (단, retry_number = 1일 때는 backoff time = 0)
                # 참고 : https://github.com/urllib3/urllib3/blob/745b002e3476f6c4ab707a2b1c82875038249be0/src/urllib3/util/retry.py#L296
                retries = Retry(total=self.max_retry, backoff_factor=0.05, status_forcelist=[ 500, 502, 503, 504 ])
                adapter = HTTPAdapter(max_retries=retries)
                s.mount('http://', adapter)
                s.mount('https://', adapter)
                response = s.get(endpoint, headers = headers)
                if response.status_code == 200:
                    messages_to_handle.append(message)
                elif response.status_code < 500: # 400대 에러일 때는 확실히 유효하지 않은 메세지로 판단
                    logger.warning(f'error from check message validation / response status_code {response.status_code}: {response.text} \n poll function will return None.', event = Event.POLL)
                    messages_to_delete.append(message)
                else: # 5회 재시도해도 500대 에러일 때는 유효한지 알 수 없으므로 유효하지 않은 메세지로 판단
                    logger.error(f'error from check message validation / response status_code {response.status_code}: {response.text} \n poll function will return None.', event = Event.POLL)
                    messages_to_handle.append(message)
        try:
            if (len(messages_to_delete) > 0):
                self.delete_messages(list(map(lambda x: x['id'], messages_to_delete)))
                logger.info(
                    message = f"Deleted {len(messages_to_delete)} invalid messages: {messages_to_delete}"
                )
            return messages_to_handle
        except Exception as e:
            logger.error(f"Error while validating evaluate message\n{e}", event = Event.POLL)

    def poll(self, max_number_of_messages = 1, mock=True):
        if get_shutdown_requested():
            logger.info(
                "System shutdown gracefully",
                event = Event.SHUTDOWN
            )
            if self.use_kafka:
                self.kafka_consumer.close()
            sys.exit(0)
        if not isinstance(max_number_of_messages,int): TypeError("max_number_of_messages is not a int")
        if not isinstance(mock, bool): TypeError("mock is not a bool")
        if mock:
            logger.info(
                "return mock",
                data = self.mock
            )
            return self.mock
        
        if self.use_kafka:
            record = self.kafka_consumer.poll(
                timeout_ms=5000,
                max_records=max_number_of_messages,
                update_offsets=False,
            )
            
            ret = []
            # 1개만 받아온 경우
            v = record.values()
            for messages in v:
                if not isinstance(messages, list):
                    logger.error(f"unexpected kafka message format: {type(message)}")
                    break
                for message in messages:
                    try:
                        message_dict = json.loads(message.value.decode('utf-8'))
                    except json.JSONDecodeError:
                        # TODO: 현재 로직이면 이 경우 offset skip 됨, 잘못된 동작은 아닌 듯 하나 체크 필요
                        logger.error("유효한 JSON 형식이 아닙니다.")
                        continue
                    ret.append(message_dict)

            # TODO: filter_valid kafka에도 구현 (receiptHandle은 필요 없으나, 경우에 따라 불필요한 메세지 제거)

            if len(ret) == 0:
                return None
            elif len(ret) == 1:
                logger.info(
                    message = f"return kafka item: {ret[0]}",
                    event = Event.POLL,
                    data = ret[0]
                )
                set_context_evaluate(
                    evaluate_id=ret[0]['id'],
                    account_id=ret[0]['accountId']
                )
                sentry_sdk.set_context("context",asdict(get_context()))
                self.poll_time = time.time()
                return ret[0]
            else:
                logger.info(
                    message = f"return kafka item: {ret}",
                    event = Event.POLL,
                    data = ret
                )
                self.poll_time = time.time()
                return ret

        elif self.use_sqs:
            response = self.sqs.receive_message(
                QueueUrl = self.queue_url,
                MaxNumberOfMessages = max_number_of_messages,  # 가져올 메시지의 최대 수 (1개 이상 설정 가능)
            )
            ret = []
            messages = response.get('Messages', [])
            for message in messages:
                message_body = message['Body']
                try:
                    # message_body를 딕셔너리로 변환
                    message_dict = json.loads(message_body)
                except json.JSONDecodeError:
                    logger.error("유효한 JSON 형식이 아닙니다.")
                self.evaluates[message_dict['id']] = message['ReceiptHandle']
                ret.append(message_dict)
            
            ret = self.filter_valid(ret)
            if len(ret) == 0:
                return None
            elif len(ret) == 1:
                logger.info(
                    message = f"return sqs item: {ret[0]}",
                    event = Event.POLL,
                    data = ret[0]
                )
                set_context_evaluate(
                    evaluate_id=ret[0]['id'],
                    account_id=ret[0]['accountId']
                )
                sentry_sdk.set_context("context",asdict(get_context()))
                self.poll_time = time.time()
                return ret[0]
            else:
                logger.info(
                    message = f"return sqs item: {ret}",
                    event = Event.POLL,
                    data = ret
                )
                self.poll_time = time.time()
                return ret

        else:
            time.sleep(0.2)
            url = f"{self.evaluate_url}/poll"

            headers = {
            'token': self.token
            }
            try:
                response = requests.request("GET", url, headers=headers, timeout=10)
            except requests.exceptions.Timeout:
                logger.warning(f'error from poll / time-out \n poll function will return None.')
                return None
            if response.status_code == 422:
                return None
            elif response.status_code != 200:
                logger.warning(f'error from poll / response status_code {response.status_code}: {response.text} \n poll function will return None.')
                return None
            logger.info(
                message = "return poll item",
                event = Event.POLL,
                data = response.json()
            )
            set_context_evaluate(
                evaluate_id=response.json()['id'],
                account_id=response.json()['accountId']
            )
            sentry_sdk.set_context("context",asdict(get_context()))
            self.poll_time = time.time()
            return response.json()

    def update_poll(self):
        '''
        data update의 경우 kafka로부터 data update event가 담긴 메세지를 받아온다.
        '''
        record = self.kafka_consumer.poll(
            timeout_ms=5000,
            max_records=1,
            update_offsets=True, # poll 하자마자 commit을 바로 하는게 아니라, commit시 자동으로 offset을 업데이트
        )
        
        ret = []
        self.record = record
        v = record.values()
        for messages in v:
            if not isinstance(messages, list):
                logger.error(f"unexpected kafka message format: {type(message)}")
                break
            for message in messages:
                try:
                    message_dict = json.loads(message.value.decode('utf-8'))
                except json.JSONDecodeError:
                    logger.error("유효한 JSON 형식이 아닙니다.")
                    continue
                # TODO(XXX): evaluates key 관리 필요 없다면 제거, commit 할 때 지워주지 않고 있음
                self.evaluates[message.key] = message.offset
                ret.append(message_dict['payload'])

        if len(ret) == 0:
            return None
        elif len(ret) == 1:
            logger.info(
                message = f"return kafka item: {ret[0]}",
                event = Event.POLL,
                data = ret[0]
            )
            self.poll_time = time.time()
            return ret[0]
        else:
            logger.info(
                message = f"return kafka item: {ret}",
                event = Event.POLL,
                data = ret
            )
            self.poll_time = time.time()
            return ret
        
    def update_complete(self, output={}, alert = False):
        '''
        data update 파이프라인에서의 validate이라고 보면 된다.
        update가 끝난뒤 이 함수를 통해서 kafka의 offset을 commit한다.
        원한다면 slack alert를 보낼 수 있다.
        '''
        self.kafka_consumer.commit()
        logger.info(
            message = "update_complete payload",
            event = Event.VALIDATE,
            data = output
        )
        if alert:
            self.slack_alert(
                '#alert_data_update',
                f"update_complete payload for topic: {self.kafka_topic} - result: {output}"
            )
        
    def update_error(self, output={}, alert = False):
        '''
        data update 파이프라인에서의 validate_error이라고 보면 된다.
        update 도중 에러가 발생했을 때 이 함수를 통해서 kafka의 offset을 commit한다.
        원한다면 slack alert를 보낼 수 있다.
        '''
        self.kafka_consumer.commit()
        logger.info(
            message = "update_error payload",
            event = Event.VALIDATE_ERROR,
            data = output
        )
        if alert:
            self.slack_alert(
                '#alert_data_update',
                f"update_error payload for topic: {self.kafka_topic} - result: {output}"
            )
        
    def validate(self, evaluate_id, output, mock=True, log=True, inference_time=None, usage=1):
        try:
            if mock:
                logger.info(message = f"validate payload - {output}")
                return
            if inference_time == None and self.poll_time != None:
                inference_time = time.time() - self.poll_time
                self.poll_time = None
            if self.use_kafka:
                try:
                    self.kafka_consumer.commit()
                except Exception as e:
                    logger.error(f"error from kafka commit\n{e}")
            elif self.use_sqs:
                try: 
                    response = self.sqs.delete_message(
                        QueueUrl = self.queue_url,
                        ReceiptHandle = self.evaluates[evaluate_id]
                    )
                except Exception as e:
                    logger.error(f"error from sqs.delete_message\n{e}")
                    del self.evaluates[evaluate_id]

            payload = json.dumps({
                "id": evaluate_id,
                "json": output
            })

            url = f"{self.evaluate_url}/validate"

            headers = {
                'token': self.token,
                'Content-Type': 'application/json'
            }

            if log:
                logger.info(
                    message = "validate payload",
                    event = Event.VALIDATE,
                    properties = {
                        "evaluate_id": evaluate_id,
                        "inference_time": inference_time,
                    },
                    data = output
                )
            with requests.Session() as s:
                retries = Retry(total=self.max_retry, backoff_factor=0.05, status_forcelist=[ 500, 502, 503, 504 ])
                adapter = HTTPAdapter(max_retries=retries)
                s.mount('http://', adapter)
                s.mount('https://', adapter)
                response = s.put(url, headers=headers, data=payload, params={'usage': usage})
                if response.status_code == 200:
                    return
                else:
                    message = f'error from validate / response status_code {response.status_code}: {response.text}'
                    sentry_sdk.capture_message(message)
                    raise Exception(message)
        finally:
            clear_context_evaluate()
        
    def validate_error(self, evaluate_id, output, mock=True, error_code=BaseStatusCode.INTERNAL_ERROR):
        try:
            if not isinstance(evaluate_id, int): raise TypeError('evaluate_id is not a int')
            if not isinstance(output, dict): raise TypeError('output is not a dict')
            if not isinstance(mock, bool): raise TypeError('mock is not a bool')
            output["code"] = error_code.value
            try:
                payload = json.dumps({
                    "id": evaluate_id,
                    "json": output
                })
            except Exception as e:
                Exception("failed to parse validate_error input : ", e)
            if mock:
                logger.info(message = f"validate_error payload - {output}")
                return

            if self.use_kafka:
                try:
                    self.kafka_consumer.commit()
                except Exception as e:
                    self.kafka_consumer.commit(f"error from kafka.commit\n{e}")
            elif self.use_sqs:
                try: 
                    response = self.sqs.delete_message(
                        QueueUrl = self.queue_url,
                        ReceiptHandle = self.evaluates[evaluate_id]
                    )
                except Exception as e:
                    logger.error(f"error from sqs.delete_message\n{e}")
                    del self.evaluates[evaluate_id]

            payload = json.dumps({
                "id": evaluate_id,
                "error": output
            })

            url = f"{self.evaluate_url}/error"

            headers = {
                'token': self.token,
                'Content-Type': 'application/json'
            }

            logger.info(
                message = "validate_error payload",
                event = Event.VALIDATE_ERROR,
                properties = {
                    "evaluate_id": evaluate_id,
                },
                data = output
            )

            with requests.Session() as s:
                retries = Retry(total=self.max_retry, backoff_factor=0.05, status_forcelist=[ 500, 502, 503, 504 ])
                adapter = HTTPAdapter(max_retries=retries)
                s.mount('http://', adapter)
                s.mount('https://', adapter)
                response = s.put(url, headers=headers, data=payload)
                if response.status_code == 200:
                    return
                else:
                    message = f'error from validate_error / response status_code {response.status_code}: {response.text}'
                    sentry_sdk.capture_message(message)
                    raise Exception(message)
        finally:
            clear_context_evaluate()

    def internal_call(self, service_code:str, key:str, metadata:dict, polling_interval=0.5, time_out=60):
        '''
        service_code : 서비스 코드
        key : key
        metadata : 요청할 메타데이터
        polling_interval : 폴링 간격
        max_polling_time : 최대 폴링 횟수
        '''
        header = {
            'X-Api-Key': os.environ.get('INTERNAL_X_API_KEY'),
            'Content-Type': 'application/json'
        }
        url = os.path.join(self.base_url, f'partner/polling/{service_code}/{key}')
        with requests.Session() as s:
            retries = Retry(total=self.max_retry, backoff_factor=0.05, status_forcelist=[ 500, 502, 503, 504 ])
            adapter = HTTPAdapter(max_retries=retries)
            s.mount('http://', adapter)
            s.mount('https://', adapter)
            response = s.post(url, headers=header, data=json.dumps(metadata))
            if response.status_code == 200:
                eval_id = response.json()['id']
            else:
                message = f'error from internal_call(post) / response status_code {response.status_code}: {response.text}'
                sentry_sdk.capture_message(message)
                raise Exception(message)
        while time_out > 0:
            time.sleep(polling_interval)
            time_out -= polling_interval
            with requests.Session() as s:
                retries = Retry(total=self.max_retry, backoff_factor=0.05, status_forcelist=[ 500, 502, 503, 504 ])
                adapter = HTTPAdapter(max_retries=retries)
                s.mount('http://', adapter)
                s.mount('https://', adapter)
                response = s.get(os.path.join(self.base_url, f'partner/{service_code}/{key}/{eval_id}'), headers=header)
                if response.status_code == 202:
                    continue
                elif response.status_code == 200:
                    if response.json()['success'] == True:
                        return response.json()['payload']
                    else:
                        message = f'error response from internal_call(get) / response status_code {response.status_code}: {response.text}'
                        sentry_sdk.capture_message(message)
                        raise Exception(message)
                else:
                    message = f'error from internal_call(get) / response status_code {response.status_code}: {response.text}'
                    sentry_sdk.capture_message(message)
                    raise Exception(message)
        message = f'internal_call timeout'
        sentry_sdk.capture_message(message)
        raise Exception(message)

    def download_from_url(self, url):
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            raise Exception(f"can't download from url {r.status_code} : {r.text}")
        else:
            return io.BytesIO(r.content)
            # return Image.open(io.BytesIO(r.content)).convert('RGB')


    def download_from_s3(self, bucket, key, download_path):
        try:
            self.s3.download_file(bucket, key, download_path)
        except Exception as e:
            raise Exception(f"failed to download from s3\n{e}")


    def upload_s3(self, upload_path, bucket, key = None, account_id = None):
        if key is None and account_id is not None:
            if not isinstance(account_id, int): raise TypeError('account_id is not a int')
            key = f"channel_id={account_id}/{time.strftime('y=%Y/m=%m/d=%d', time.localtime(time.time()))}/{os.path.basename(upload_path)}"
        try:
            self.s3.upload_file(upload_path, bucket, key)
            logger.info(
                message = f"uploaded to s3://{bucket}/{key}",
                event = Event.UPLOAD_S3,
            )
            return os.path.join(f"https://{bucket}.s3.ap-northeast-2.amazonaws.com", key)
        except Exception as e:
            raise Exception(f"failed to upload s3\n{e}")


    def upload_s3_image(self, pil_image, bucket, img_save_name = None, key = None, account_id = None):
        '''
        pil_image : PIL.Image
        bucket : S3에 업로드할 버킷 이름
        img_save_name : S3에 저장될 이미지 파일 이름
        key : S3에 저장될 이미지 파일 경로
        account_id : S3에 저장될 이미지 파일 경로에 포함될 account_id
        '''
        img_byte_arr = io.BytesIO()
        if img_save_name is None and key is None:
            raise ValueError("img_save_name or key is required")
        if img_save_name is not None:
            if not isinstance(account_id, int): raise TypeError('account_id is not a int')
            output_file_extension = img_save_name.split('.')[-1]
            key = f"channel_id={account_id}/{time.strftime('y=%Y/m=%m/d=%d', time.localtime(time.time()))}/{img_save_name}"
        else:
            output_file_extension = key.split('.')[-1]
        
        pil_image.save(img_byte_arr, format=str(output_file_extension).upper())
        img_byte_arr = img_byte_arr.getvalue()
        
        try:
            self.s3.put_object(Body=img_byte_arr, Bucket="dalpha-internal-demo", Key=key)
            logger.info(
                message = f"uploaded to s3://{bucket}/{key}",
                event = Event.UPLOAD_S3,
            )
            return os.path.join(f"https://{bucket}.s3.ap-northeast-2.amazonaws.com", key)
        except Exception as e:
            raise Exception(f"failed to upload s3\n{e}")


    def slack_alert(self, channel_name, text):
        '''
        channel_name : slack 채널 id 또는 #채널명
        text : 보낼 메세지
        원하는 slack channel에 메세지를 보내는 함수
        '''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer xoxb-4286174283573-6855321848326-Z2QnHswtlITp5gNQj7eXVHjP'
        }
        payload = {
            "channel": channel_name,
            "text": text
        }
        response = requests.request("POST", 'https://slack.com/api/chat.postMessage', headers=headers, data=json.dumps(payload))
        if response.status_code != 200:
            logger.warning(f'error from slack_alert / response status_code {response.status_code}: {response.text}')
