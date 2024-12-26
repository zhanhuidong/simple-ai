import os
import sys

import uvicorn
import time
from fastapi import Request, FastAPI, Query
from starlette.types import ASGIApp
from starlette.responses import StreamingResponse
import threading

import logging as logger


# app = App.createApp()
app = FastAPI(title ='simple-ai', description = '简易ai的组件服务')


@app.get('/simple-ai/ok')
def ok(name:str = Query()) -> str:

    return app.components_data[name]

def on_start_up():
    from core import components_loader
    components_loader.load_classes_from_components()
    app.components_data = components_loader.load_classes_from_components()  # 绑定加载的数据到app上

if __name__ == '__main__':
    try:
        logger.info("开始启动服务======")

        #启动线程做一些额外工作
        threading.Thread(target = on_start_up).start()

        uvicorn.run(app, host='0.0.0.0', port=8899)
    except Exception as e:
        logger.exception("server start error:{}".format(e))
