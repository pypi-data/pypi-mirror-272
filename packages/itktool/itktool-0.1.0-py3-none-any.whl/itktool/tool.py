import argparse
from langchain_openai import ChatOpenAI
from datetime import datetime
from langchain_community.callbacks import get_openai_callback
from langchain_community.callbacks.manager import get_bedrock_anthropic_callback

from langchain_anthropic import ChatAnthropic
# from langchain_community.llms

#  监控
#  1. 不同平台 -p str
#  2. 测试key -k int   
#  3. 不同模型 -m str 
#  4. 并发数据 -c int    



KIMI_BASE_URL = "https://api.moonshot.cn/v1"


def run():
    parser = argparse.ArgumentParser(description='iTinkAi command line production!')
    parser.add_argument('api_key', help='Test your LLM key.')
    parser.add_argument('-pl', '--platform_llm', help='this is platfrom e.g. "chatgpt", "kimi", "calude"')
    parser.add_argument('-m', '--model', help='this is llm model')
    # parser.add_argument('-c', '--count', type=int, help='') # 并发
    
    args = parser.parse_args()

    # test 
    # print(type(args))
    # print(args.api_key)
    # print(args.model)
    # print(args.platform_llm)
    # print(args.key)
    print(args)

    if args is None:
        print("there is no vailed parameter!")

    if args.api_key:
        if args.platform_llm == "chatgpt":
            if args.model:
                check_openai_key(api_key=args.api_key, model_name=args.model)
            else:
                check_openai_key(api_key=args.api_key)
        elif args.platform_llm == "kimi":
            if args.model:
                print("tt ")
                check_kimi_key(api_key=args.api_key, model_name=args.model)
            else:
                print("t ")
                check_kimi_key(api_key=args.api_key)
        elif args.platform_llm == "claude":
            if args.model:
                check_kimi_key(api_key=args.api_key, model_name=args.model)
            else:
                check_kimi_key(api_key=args.api_key)
        else:
            if args.model:
                check_openai_key(api_key=args.api_key, model_name=args.model)
            else:
                check_openai_key(api_key=args.api_key)
    else:
        print("please input your key to test!")

            
            
def check_openai_key(**kwargs):
    current_time = datetime.now()
    llm = ChatOpenAI(model_name="gpt-4-turbo", api_key=kwargs.get('api_key'))
    with get_openai_callback() as cb:
        result = llm.invoke("hello")
        print(f"输入消耗token: {cb.prompt_tokens}")
        print(f"输出消耗token: {cb.completion_tokens}")
        print(f"总消耗token: {cb.total_tokens}")
        print(f"费用($): {cb.total_cost}")
        print(f"耗时: {datetime.now()-current_time}")
                

def check_kimi_key(**kwargs):
    current_time = datetime.now()
    llm = ChatOpenAI(model_name="moonshot-v1-8k", api_key=kwargs.get('api_key'), base_url=KIMI_BASE_URL)
    with get_openai_callback() as cb:
        result = llm.invoke("hello")
        print(f"输入消耗token: {cb.prompt_tokens}")
        print(f"输出消耗token: {cb.completion_tokens}")
        print(f"总消耗token: {cb.total_tokens}")
        print(f"费用(￥): {cb.total_cost}")
        print(f"耗时: {datetime.now()-current_time}")


def check_claude_key(**kwargs): 
    current_time = datetime.now()
    llm = ChatAnthropic(model_name="claude-3-opus-20240229", api_key=kwargs.get('api_key'))
    with get_bedrock_anthropic_callback() as cb:
        result = llm.invoke("hello")
        print(f"输入消耗token: {cb.prompt_tokens}")
        print(f"输出消耗token: {cb.completion_tokens}")
        print(f"总消耗token: {cb.total_tokens}")
        print(f"费用（$）: {cb.total_cost}")
        print(f"耗时: {datetime.now()-current_time}")



if __name__ == "__main__":
    run()