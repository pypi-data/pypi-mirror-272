_H='CustomStreamWrapper'
_G='Stream'
_F=False
_E='put'
_D='local'
_C='prod'
_B='PACKAGE_ENV'
_A=None
__version__='0.1.37'
import datetime,os,inspect,copy,time,math,json
from typing import List,Union,Any,Literal
from urllib import response
from regex import D
import requests
from dataclasses import dataclass,asdict
from composo.package_primitives import*
from composo.helpers import parse_parameters,generate_api_key,parse_return_type,stream_handler
from typing import ClassVar,Dict,Protocol,Any
import logging
from colorama import init,Fore
init()
def conditional_raise(x):
	'\n    Allow errors to be raised in local\n    '
	if os.environ.get(_B,_C)==_D:raise x
def check_is_jsonable(x):
	recreated_json=json.loads(json.dumps(x))
	if not recreated_json==x:raise ValueError('Result must be parsable JSON')
class ComposoLogHandler(logging.StreamHandler):
	def __new__(cls,*args,**kwargs):return super(ComposoLogHandler,cls).__new__(cls)
	def __init__(self,stream=_A):super().__init__(stream)
	def emit(self,record):record.msg=f"{Fore.YELLOW}Composo:{Fore.RESET} {record.msg}";super().emit(record)
packageLogger=logging.getLogger('ComposoLogger')
if os.environ.get(_B,_C)in[_D,'dev']:print("Using DEBUG logging as you're running locally");packageLogger.setLevel(logging.DEBUG)
else:packageLogger.setLevel(logging.INFO)
if os.environ.get(_B,_C)==_D:packageLogger.info('Connecting to Composo local');BACKEND_URL='http://localhost:8000';FRONTEND_URL='http://localhost:5173'
elif os.environ.get(_B,_C)=='dev':packageLogger.info('Connecting to Composo dev');BACKEND_URL='https://composo-prod-backend-composo-dev-backend.azurewebsites.net';FRONTEND_URL=BACKEND_URL
elif os.environ.get(_B,_C)=='test':packageLogger.info('Connecting to Composo test');BACKEND_URL='http://composo-prod-backend-composo-test-backend.azurewebsites.net';FRONTEND_URL=BACKEND_URL
else:BACKEND_URL='https://app.composo.ai';FRONTEND_URL=BACKEND_URL
handler=ComposoLogHandler()
formatter=logging.Formatter('%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
packageLogger.addHandler(handler)
class IsDataclass(Protocol):__dataclass_fields__:0
def make_request(method,path,data=_A,timeout=100,max_tries=100):
	packageLogger.debug(f"Request started path: {path}");headers={'Content-Type':'application/json'};url=BACKEND_URL+path;tries=0
	while tries<max_tries:
		try:
			if method.lower()=='post':json_data=json.dumps(asdict(data),default=str);response=requests.post(url,data=json_data,headers=headers,timeout=timeout)
			elif method.lower()=='get':response=requests.get(url,headers=headers,timeout=timeout)
			elif method.lower()==_E:json_data=json.dumps(asdict(data),default=str);response=requests.put(url,data=json_data,headers=headers,timeout=timeout)
			else:raise ValueError('Invalid method. Available options are "post", "get", and "put".')
			if tries>0:packageLogger.info('Connection to Composo backend re-established')
			packageLogger.debug(f"Request finished path: {path}");return response
		except requests.exceptions.Timeout as e:packageLogger.info(f"Request to Composo timed out. Retry {tries+1} of {max_tries}");time.sleep(max(10*(tries/10)**2,10));tries+=1
		except requests.exceptions.ConnectionError as e:packageLogger.info(f"Could not connect to Composo. Retry {tries+1} of {max_tries}");time.sleep(max(10*(tries/10)**2,10));tries+=1
		except Exception as e:raise ComposoDeveloperException(f"There was an unexpected error in make request: {str(e)}")
	raise ComposoCriticalException(f"Could not connect to Composo backend after {max_tries} tries.")
class BackendEventGress:
	@staticmethod
	def update_last_active(runner_id):make_request(_E,path=f"/api/runner/{runner_id}",data=RunnerUpdate(last_active=datetime.datetime.now(datetime.timezone.utc)))
	def event_poll(self,this_runner_id):
		A='message';response=make_request(method='get',path=f"/api/runner/package/{this_runner_id}")
		if response.status_code==200:
			json_response=response.json()
			try:
				parsed_event=PollResponse(**json_response)
				try:trigger=RunTrigger(**parsed_event.payload);cases=[CaseTrigger(**x)for x in trigger.cases];trigger.cases=cases;parsed_event.payload=trigger;return parsed_event
				except:pass
				try:parsed_event.payload=AppDeletionEvent(**parsed_event.payload);return parsed_event
				except:pass
				parsed_event.payload=_A;return parsed_event
			except Exception as e:raise ComposoDeveloperException(f"Could not parse the response from the backend into a known response type: {response}")
		elif response.status_code==418:packageLogger.error(f"ERROR: {response.json()[A]}")
		elif response.status_code==501:ComposoDeveloperException(f"POLLING ERROR: {response.json()[A]}")
		else:raise ComposoDeveloperException(f"The backend is returning an unknown error from polling: {response}")
	def report_run_results(self,run_result,run_id):
		response=make_request(_E,path=f"/api/runner/package/{run_id}",data=run_result)
		if response.status_code==200:packageLogger.info('Run completed and results reported')
		else:raise ComposoDeveloperException(f"The backend is returning a non 200 status code from reporting run results, this should never happen: {response}")
	def register_runner(self,api_key,adjustable_params,auto_bump,version,docstring):response=make_request('post','/api/runner',data=RunnerCreate(api_key=api_key,parameters=adjustable_params,runner_type='python',package_version=__version__,docstring=docstring,auto_bump=auto_bump,version=version),max_tries=1);return response
def run_experiment(replacement_vars,all_vars,func):
	'\n    Takes a dict replacement_vars where both values are json str dump, conversion to the correct type is handled inside\n    ';packageLogger.info('Experiment initiated')
	if not all(key in[x.name for x in all_vars]for key in replacement_vars.keys()):raise ComposoDeveloperException(f"The user has somehow been allowed to provide args that are not tagged. Provided args: {replacement_vars.keys()}. Tagged args: {[x.name for x in all_vars]} ")
	working_args=[];working_kwargs={}
	for arg in copy.deepcopy(all_vars):
		pushme=lambda x:working_args.append(x)if not arg.is_kwarg else working_kwargs.update({arg.name:x})
		def typeme(x):
			try:return arg.cast(x)
			except Exception as e:raise ComposoUserException(f"The provided arg could not be converted to required type: {arg.param_type}. Arg value was {x}")
		validate_me=lambda x:arg.validate(x)
		if type(arg)==FixedParameter:pushme(arg.live_working_value)
		elif arg.name in replacement_vars:typed=typeme(replacement_vars[arg.name]);validate_me(typed);pushme(typed)
		else:typed=typeme(arg.demo_value);validate_me(typed);pushme(typed)
	try:ret_val=func(*working_args,**working_kwargs)
	except Exception as e:raise ComposoUserException(f"The linked function produced an error: {str(e)}")
	return ret_val
def experiment_controller(func,demo_args,demo_kwargs,demo_globals,api_key='cp-XXX_FAKE_KEY_FOR_TESTING_XXXX',auto_bump=_F,version=_A,event_gress=_A,poll_wait_time=3):
	C='########################################';B='POLL_WAIT_TIME';A='id'
	if os.environ.get(B)is not _A:
		try:_poll_wait_time=int(os.environ.get(B));assert _poll_wait_time>=1 and _poll_wait_time<10;poll_wait_time=_poll_wait_time
		except:pass
	if event_gress is _A:
		packageLogger.info('Initialising live connection to Composo')
		if api_key is _A:raise ValueError('api_key must be provided')
		event_gress=BackendEventGress()
	packageLogger.info('Composo Experiment is activated');all_vars=parse_parameters(func,*demo_args,**demo_kwargs);return_type=parse_return_type(func);app_is_streaming=return_type in[_G,_H];adjustable_params=[x for x in all_vars if type(x)in WORKABLE_TYPES.__args__];docstring=inspect.getdoc(func);response=event_gress.register_runner(api_key,adjustable_params,auto_bump,version,docstring)
	if response.status_code!=200:raise ComposoDeveloperException(f"Could not register runner: {response.json()}")
	this_runner=response.json();packageLogger.info(C);packageLogger.info('# FOLLOW THE LINK TO REGISTER YOUR APP #');packageLogger.info(f"{Fore.CYAN}"+FRONTEND_URL+'/link?api_key='+api_key+f"{Fore.RESET}");packageLogger.info('######### Or use your API key ##########');packageLogger.info('### '+api_key+' ###');packageLogger.info(C);previously_noted_app_ids=[];packageLogger.info('Connected and listening.')
	while True:
		try:
			time.sleep(poll_wait_time);BackendEventGress.update_last_active(this_runner[A]);event=event_gress.event_poll(this_runner[A])
			if isinstance(event,PollResponse):
				if isinstance(event.payload,AppDeletionEvent):packageLogger.critical('Composo is shutting down.');packageLogger.critical(event.payload.message);return
				registered_apps=event.registered_apps
				for registered_app in registered_apps:
					if registered_app not in previously_noted_app_ids:packageLogger.info(f"App registered: {registered_app}");previously_noted_app_ids.append(registered_app)
				if event.payload is not _A:
					packageLogger.info('New Evaluation Run Triggered')
					def report_case(case):event_gress.report_run_results(RunResult(run_id=event.payload.run_id,results=[case]),run_id=event.payload.run_id)
					packageLogger.info(f"Running {len(event.payload.cases)} cases")
					for case in event.payload.cases:
						BackendEventGress.update_last_active(this_runner[A]);case_result=_A
						try:
							ret=run_experiment(case.vars,all_vars,func)
							if app_is_streaming:
								if not hasattr(ret,'__iter__'):raise ComposoUserException('The linked function is returning a stream but the return type is not iterable.')
								report_case_intermediate=lambda current_value:report_case(CaseResult(case_id=case.case_id,value=current_value,error=_A,output_stream_incomplete=True));final_result=stream_handler(ret,report_case_intermediate)
							else:final_result=ret
							case_result=CaseResult(case_id=case.case_id,value=final_result,error=_A,output_stream_incomplete=_F);print('Setting output_stream_incomplete to False');print(case_result);report_case(case_result)
						except ComposoUserException as e:conditional_raise(e);case_result=CaseResult(case_id=case.case_id,value=_A,error='ERROR: '+str(e));report_case(case_result)
						except Exception as e:conditional_raise(e);packageLogger.debug(f"Unidentified exception caught with case {case}: {str(e)}");case_result=CaseResult(case_id=case.case_id,value=_A,error='ERROR: The composo package has failed with an unidentified error. Please contact composo support.');report_case(case_result)
		except ComposoDeveloperException as e:conditional_raise(e);packageLogger.debug(f"Composo Developer Exception caught: {str(e)}");pass
		except ComposoUserException as e:conditional_raise(e);packageLogger.info(f"Composo User Exception caught: {str(e)}")
		except ComposoCriticalException as e:conditional_raise(e);raise e
		except Exception as e:conditional_raise(e);packageLogger.debug(f"Unidentified exception caught: {str(e)}");pass
class Composo:
	@classmethod
	def link(cls,api_key=_A,auto_bump=_F,version=_A):
		def actual_decorator(func):
			def wrapped_func(*args,**kwargs):
				A='COMPOSO_APP_API_KEY'
				if not hasattr(Composo,'activated'):
					cls.api_key=api_key;cls.auto_bump=auto_bump;cls.version=version;cls.activated=True;packageLogger.info('Composo is activated. Running the function once to check for errors...')
					try:result=func(*args,**kwargs)
					except Exception as e:raise Exception('The function invocation has errors. Please fix before linking to Composo. Error: '+str(e))
					permissable_return_types=['int','float','str','dict','list','tuple',_H,_G];result_type=type(result).__name__
					if result_type not in permissable_return_types:raise Exception(f"The linked function returned type: {result_type}. Supported return types are {', '.join(permissable_return_types)}")
					packageLogger.info('Function test run successful.')
					if cls.api_key is _A:
						if A in os.environ:cls.api_key=os.environ[A]
						else:cls.api_key=generate_api_key()
					experiment_controller(func,args,kwargs,func.__globals__,api_key=cls.api_key,auto_bump=cls.auto_bump,version=cls.version);return result
				else:result=func(*args,**kwargs)
			return wrapped_func
		return actual_decorator