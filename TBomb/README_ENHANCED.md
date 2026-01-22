# TBomb Enhanced 🚀

An enhanced version of TBomb with async implementation, API health monitoring, database integration, and Docker support.

## 🆕 New Features

- **Async Implementation**: Better performance with concurrent requests
- **API Health Monitoring**: Automatic endpoint health checking
- **Database Integration**: SQLite database for API management
- **Docker Support**: Easy containerized deployment
- **Enhanced Error Handling**: Robust error management
- **Real-time Monitoring**: Continuous API health monitoring

## 🏗️ Architecture

```
TBomb Enhanced/
├── database/           # Database models and management
├── health/            # API health checking
├── utils/             # Enhanced utilities
├── bomber_async.py    # Main async application
├── health_monitor.py  # Health monitoring service
├── setup.py          # Setup script
├── Dockerfile        # Docker configuration
└── docker-compose.yml # Docker Compose setup
```

## 🚀 Quick Start

### Local Installation

1. **Setup Environment**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-async.txt
   python setup.py
   ```

2. **Run Application**
   ```bash
   # Interactive mode
   python bomber_async.py
   
   # CLI mode
   python bomber_async.py --sms
   ```

3. **Start Health Monitor**
   ```bash
   python health_monitor.py
   ```

### Docker Deployment

1. **Build and Run**
   ```bash
   docker-compose up -d
   ```

2. **Interactive Mode**
   ```bash
   docker-compose exec tbomb python bomber_async.py
   ```

## 📊 Database Features

- **API Endpoint Management**: Store and manage API configurations
- **Health Tracking**: Track API response times and success rates
- **Performance Analytics**: Monitor API performance over time
- **Automatic Cleanup**: Remove unhealthy endpoints

## 🔍 Health Monitoring

- **Continuous Monitoring**: 24/7 API health checking
- **Automatic Recovery**: Re-enable healthy APIs
- **Performance Metrics**: Response time and success rate tracking
- **Alert System**: Notifications for API failures

## ⚡ Performance Improvements

- **Async Requests**: Up to 10x faster than synchronous version
- **Connection Pooling**: Efficient HTTP connection management
- **Smart Rate Limiting**: Prevent API overload
- **Concurrent Processing**: Multiple requests simultaneously

## 🐳 Docker Features

- **Multi-service Setup**: Main app + health monitor
- **Volume Persistence**: Data and logs persistence
- **Auto-restart**: Automatic service recovery
- **Resource Limits**: Controlled resource usage

## 📈 Usage Examples

### Basic SMS Bombing
```bash
python bomber_async.py --sms
# Enter country code: 91
# Enter target: 9876543210
# Enter count: 50
# Enter delay: 1
# Enter concurrent: 5
```

### Health Check
```bash
python health_monitor.py --once
```

### Docker Deployment
```bash
docker-compose up -d
docker-compose logs -f tbomb
```

## 🔧 Configuration

### Environment Variables
- `DATABASE_PATH`: Database file path
- `LOG_LEVEL`: Logging level (INFO, DEBUG, ERROR)
- `HEALTH_CHECK_INTERVAL`: Health check interval in seconds

### Database Schema
- `api_endpoints`: API configuration storage
- `api_health`: Health check results and metrics

## 🛡️ Security Features

- **Input Validation**: Comprehensive input sanitization
- **Rate Limiting**: Built-in abuse protection
- **Error Handling**: Secure error management
- **Container Security**: Non-root user execution

## 📋 Requirements

### Python Dependencies
- aiohttp>=3.8.0
- aiosqlite>=0.17.0
- requests>=2.24.0
- colorama>=0.4.3

### System Requirements
- Python 3.7+
- Docker (optional)
- 512MB RAM minimum

## ⚠️ Ethical Usage

This tool is for educational and testing purposes only. Always ensure you have explicit permission before testing on any systems you don't own.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Original TBomb by TheSpeedX
- Enhanced by the community
- Built with modern Python async patterns