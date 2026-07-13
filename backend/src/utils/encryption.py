"""
API密钥加密工具模块
使用Fernet对称加密来保护API密钥
"""

import base64
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken

from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)


class EncryptionError(Exception):
    """加密相关异常"""
    pass


class EncryptionService:
    """加密服务类"""
    
    _instance: Optional['EncryptionService'] = None
    _cipher: Optional[Fernet] = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化加密服务"""
        if self._cipher is None:
            self._initialize_cipher()
    
    def _initialize_cipher(self):
        """初始化加密器"""
        # 从配置获取加密密钥
        encryption_key = settings.API_KEY_ENCRYPTION_KEY
        
        if not encryption_key:
            # 开发环境持久化自动生成的密钥，避免服务重启后已有 API Key 无法解密。
            key_file = Path(__file__).resolve().parents[2] / "data" / ".api_key_encryption_key"
            key_file.parent.mkdir(parents=True, exist_ok=True)
            if key_file.exists():
                encryption_key = key_file.read_text(encoding="utf-8").strip()
            else:
                encryption_key = Fernet.generate_key().decode()
                key_file.write_text(encryption_key, encoding="utf-8")
            logger.warning(
                "API_KEY_ENCRYPTION_KEY 未设置，使用本地持久化开发密钥。"
                "生产环境必须设置此环境变量！"
            )
        
        try:
            # 确保密钥是字节格式
            if isinstance(encryption_key, str):
                encryption_key = encryption_key.encode()
            
            self._cipher = Fernet(encryption_key)
            logger.info("加密服务初始化成功")
        except Exception as e:
            logger.error(f"加密服务初始化失败: {e}")
            raise EncryptionError(f"无法初始化加密服务: {str(e)}")
    
    def encrypt(self, plain_text: str) -> str:
        """
        加密文本
        
        Args:
            plain_text: 明文字符串
            
        Returns:
            加密后的字符串（Base64编码）
            
        Raises:
            EncryptionError: 加密失败时抛出
        """
        if not plain_text:
            raise EncryptionError("不能加密空字符串")
        
        try:
            # 将字符串转换为字节
            plain_bytes = plain_text.encode('utf-8')
            
            # 加密
            encrypted_bytes = self._cipher.encrypt(plain_bytes)
            
            # 转换为字符串返回
            encrypted_text = encrypted_bytes.decode('utf-8')
            
            return encrypted_text
        except Exception as e:
            logger.error(f"加密失败: {e}")
            raise EncryptionError(f"加密失败: {str(e)}")
    
    def decrypt(self, encrypted_text: str) -> str:
        """
        解密文本
        
        Args:
            encrypted_text: 加密的字符串
            
        Returns:
            解密后的明文字符串
            
        Raises:
            EncryptionError: 解密失败时抛出
        """
        if not encrypted_text:
            raise EncryptionError("不能解密空字符串")
        
        try:
            # 将字符串转换为字节
            encrypted_bytes = encrypted_text.encode('utf-8')
            
            # 解密
            decrypted_bytes = self._cipher.decrypt(encrypted_bytes)
            
            # 转换为字符串返回
            decrypted_text = decrypted_bytes.decode('utf-8')
            
            return decrypted_text
        except InvalidToken:
            logger.error("解密失败: 无效的加密令牌")
            raise EncryptionError("解密失败: 数据已损坏或使用了错误的密钥")
        except Exception as e:
            logger.error(f"解密失败: {e}")
            raise EncryptionError(f"解密失败: {str(e)}")
    
    def mask_api_key(self, api_key: str, visible_chars: int = 4) -> str:
        """
        遮罩API密钥，只显示部分字符
        
        Args:
            api_key: API密钥
            visible_chars: 可见字符数量
            
        Returns:
            遮罩后的API密钥
        """
        if not api_key or len(api_key) <= visible_chars:
            return "****"
        
        return f"{api_key[:visible_chars]}{'*' * (len(api_key) - visible_chars)}"


# 创建全局加密服务实例
_encryption_service = EncryptionService()


def encrypt_api_key(plain_key: str) -> str:
    """
    加密API密钥
    
    Args:
        plain_key: 明文API密钥
        
    Returns:
        加密后的API密钥
    """
    return _encryption_service.encrypt(plain_key)


def decrypt_api_key(encrypted_key: str) -> str:
    """
    解密API密钥
    
    Args:
        encrypted_key: 加密的API密钥
        
    Returns:
        明文API密钥
    """
    return _encryption_service.decrypt(encrypted_key)


def mask_api_key(api_key: str, visible_chars: int = 4) -> str:
    """
    遮罩API密钥
    
    Args:
        api_key: API密钥
        visible_chars: 可见字符数量
        
    Returns:
        遮罩后的API密钥
    """
    return _encryption_service.mask_api_key(api_key, visible_chars)


__all__ = [
    'EncryptionService',
    'EncryptionError',
    'encrypt_api_key',
    'decrypt_api_key',
    'mask_api_key',
]
