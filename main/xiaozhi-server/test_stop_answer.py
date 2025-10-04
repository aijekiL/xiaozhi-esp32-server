#!/usr/bin/env python3
"""
测试停止回答功能的脚本
"""

import asyncio
import websockets
import json
import time

async def test_stop_answer():
    """测试停止回答功能"""
    
    # 连接参数
    uri = "ws://localhost:8000/xiaozhi/v1/?device-id=test-device&client-id=test-client"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("已连接到WebSocket服务器")
            
            # 发送测试消息
            test_messages = [
                "你好，请介绍一下你自己",
                "停止回答",  # 测试停止命令
                "继续说话",  # 测试是否能继续对话
                "退出"       # 测试退出命令
            ]
            
            for i, message in enumerate(test_messages):
                print(f"\n--- 测试 {i+1}: {message} ---")
                
                # 发送文本消息
                await websocket.send(message)
                
                # 等待响应
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    print(f"收到响应: {response}")
                except asyncio.TimeoutError:
                    print("响应超时")
                
                # 等待一段时间再进行下一个测试
                await asyncio.sleep(2)
                
            print("\n测试完成")
            
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    print("开始测试停止回答功能...")
    asyncio.run(test_stop_answer())
