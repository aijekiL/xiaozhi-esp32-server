"""
停止回答处理器
用于处理用户说"停止回答"等命令，立即打断智能音箱的回复
"""

from config.logger import setup_logging

TAG = __name__
logger = setup_logging()


async def handle_stop_answer(conn, text):
    """
    处理停止回答请求
    
    Args:
        conn: 连接处理器实例
        text: 用户输入的文本
        
    Returns:
        bool: 是否成功处理了停止回答请求
    """
    try:
        # 定义停止回答的关键词
        stop_keywords = [
            "停止回答", "别说了", "闭嘴", "停止", "停", "够了",
            "stop", "stop talking", "shut up", "enough"
        ]
        
        # 检查是否包含停止关键词
        text_lower = text.lower()
        for keyword in stop_keywords:
            if keyword.lower() in text_lower:
                logger.bind(tag=TAG).info(f"检测到停止回答关键词: {keyword}")
                
                # 检查TTS状态
                if hasattr(conn, 'tts') and conn.tts:
                    logger.bind(tag=TAG).info(f"TTS状态检查: tts_stop_request={getattr(conn.tts, 'tts_stop_request', 'N/A')}")
                    logger.bind(tag=TAG).info(f"TTS队列状态: 文本队列大小={getattr(conn.tts, 'tts_text_queue', 'N/A')}, 音频队列大小={getattr(conn.tts, 'tts_audio_queue', 'N/A')}")
                else:
                    logger.bind(tag=TAG).warning("TTS组件未初始化")
                
                # 检查连接状态
                logger.bind(tag=TAG).info(f"连接状态: client_abort={getattr(conn, 'client_abort', 'N/A')}, llm_finish_task={getattr(conn, 'llm_finish_task', 'N/A')}")
                
                # 调用连接处理器的停止回答方法
                if hasattr(conn, 'stop_answering'):
                    success = conn.stop_answering()
                    if success:
                        logger.bind(tag=TAG).info("成功停止回答")
                        
                        # 再次检查状态
                        if hasattr(conn, 'tts') and conn.tts:
                            logger.bind(tag=TAG).info(f"停止后TTS状态: tts_stop_request={getattr(conn.tts, 'tts_stop_request', 'N/A')}")
                            logger.bind(tag=TAG).info(f"停止后TTS队列状态: 文本队列大小={getattr(conn.tts, 'tts_text_queue', 'N/A')}, 音频队列大小={getattr(conn.tts, 'tts_audio_queue', 'N/A')}")
                        
                        logger.bind(tag=TAG).info(f"停止后连接状态: client_abort={getattr(conn, 'client_abort', 'N/A')}, llm_finish_task={getattr(conn, 'llm_finish_task', 'N/A')}")
                        return True
                    else:
                        logger.bind(tag=TAG).error("停止回答失败")
                        return False
                else:
                    logger.bind(tag=TAG).warning("连接处理器没有stop_answering方法")
                    return False
        
        return False
        
    except Exception as e:
        logger.bind(tag=TAG).error(f"处理停止回答请求时出错: {e}")
        return False


def is_stop_answer_command(text):
    """
    判断文本是否是停止回答命令
    
    Args:
        text: 要检查的文本
        
    Returns:
        bool: 是否是停止回答命令
    """
    stop_keywords = [
        "停止回答", "别说了", "闭嘴", "停止", "停", "够了",
        "stop", "stop talking", "shut up", "enough"
    ]
    
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in stop_keywords)
