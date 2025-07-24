# Library API - DevOps Pipeline Project

A complete Flask REST API for book management with full CI/CD pipeline using GitHub Actions, Terraform, and LocalStack.

## 🚀 Features

- **Complete CRUD Operations**: Create, Read, Update, Delete books
- **In-Memory Storage**: No external database required
- **RESTful API**: Standard HTTP methods and status codes
- **Comprehensive Testing**: Unit tests with pytest
- **Infrastructure as Code**: Terraform configuration for AWS Lambda and API Gateway
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions
- **Local Development**: LocalStack for local AWS simulation
- **Production Ready**: Error handling, validation, and proper HTTP responses

## 📁 Project Structure

```
DevOps_WS/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline
├── terraform/
│   ├── main.tf                 # Terraform infrastructure configuration
│   └── lambda.zip              # Packaged Lambda function
├── tests/
│   └── test_app.py            # Unit tests
├── app.py                     # Main Flask application
├── wsgi_handler.py            # AWS Lambda WSGI handler
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # LocalStack configuration
└── README.md                  # This file
```

## 🔧 Prerequisites

- **Docker & Docker Compose**: For LocalStack
- **Python 3.8+**: For the Flask application
- **Terraform**: For infrastructure provisioning
- **Git**: For version control
- **GitHub Account**: For CI/CD pipeline

## 🏃‍♂️ Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd DevOps_WS
pip install -r requirements.txt
```

### 2. Run Tests

```bash
pytest tests/ -v
```

### 3. Start LocalStack

```bash
docker-compose up -d
```

### 4. Run Application Locally

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## 📚 API Endpoints

### Base Endpoints
- `GET /` - Welcome message and API documentation
- `GET /health` - Health check endpoint
- `GET /api/info` - API metadata and information

### Book Management
- `GET /api/books` - Get all books
- `GET /api/books/<id>` - Get book by ID
- `POST /api/books` - Create new book
- `PUT /api/books/<id>` - Update existing book
- `DELETE /api/books/<id>` - Delete book

### Example Usage

#### Get all books
```bash
curl http://localhost:5000/api/books
```

#### Create a new book
```bash
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald", 
    "genre": "Fiction",
    "year": 1925
  }'
```

#### Update a book
```bash
curl -X PUT http://localhost:5000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "year": 2023
  }'
```

#### Delete a book
```bash
curl -X DELETE http://localhost:5000/api/books/1
```

## 🏗️ Infrastructure Deployment

### LocalStack (Development)

1. **Start LocalStack**:
```bash
docker-compose up -d
```

2. **Deploy Infrastructure**:
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

3. **Verify Deployment**:
```bash
# Check if Lambda function exists
aws --endpoint-url=http://localhost:4566 lambda list-functions

# Check API Gateway
aws --endpoint-url=http://localhost:4566 apigatewayv2 get-apis
```

### AWS (Production)

Update `terraform/main.tf` to remove LocalStack endpoints and use real AWS credentials:

```hcl
provider "aws" {
  region = "us-east-1"
  # Remove localstack endpoints
}
```

## 🔄 CI/CD Pipeline

The project includes a GitHub Actions workflow that:

1. **Tests**: Runs pytest on every push to main
2. **Packages**: Creates Lambda deployment package
3. **Deploys**: Uses Terraform to deploy infrastructure
4. **Validates**: Verifies deployment success

### Setting up Self-Hosted Runner

1. Go to your GitHub repository → Settings → Actions → Runners
2. Click "New self-hosted runner"
3. Follow the setup instructions for your OS
4. Ensure the runner has:
   - Docker installed and running
   - Terraform installed
   - Python 3.8+ installed
   - Access to your LocalStack instance

### Pipeline Triggers

- **Push to main**: Full CI/CD pipeline
- **Pull Request**: Run tests only

## 🧪 Testing

### Unit Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Integration Tests
```bash
# Start the application
python app.py &

# Test endpoints
curl http://localhost:5000/health
curl http://localhost:5000/api/books
```

### Load Testing
```bash
# Install hey (HTTP load testing tool)
# Then test API performance
hey -n 1000 -c 10 http://localhost:5000/api/books
```

## 🔍 Monitoring and Debugging

### LocalStack Dashboard
Access LocalStack dashboard at `http://localhost:4566` to monitor AWS resources.

### Application Logs
```bash
# View application logs (if running in Docker)
docker logs localstack-library-api

# View Terraform state
cd terraform && terraform show
```

### Health Checks
```bash
# Application health
curl http://localhost:5000/health

# LocalStack health
curl http://localhost:4566/health
```

## 🛠️ Development

### Adding New Endpoints

1. Add route to `app.py`
2. Add corresponding tests to `tests/test_app.py`
3. Update this README documentation
4. Test locally before committing

### Modifying Infrastructure

1. Update `terraform/main.tf`
2. Run `terraform plan` to preview changes
3. Apply changes with `terraform apply`
4. Update documentation

## 🚨 Troubleshooting

### Common Issues

**LocalStack not starting**:
- Ensure Docker is running
- Check port 4566 is not in use
- Try `docker-compose down && docker-compose up`

**Tests failing**:
- Verify Python dependencies: `pip install -r requirements.txt`
- Check Flask app syntax: `python -c "from app import app"`

**Terraform apply fails**:
- Ensure LocalStack is running
- Check AWS credentials for LocalStack
- Verify terraform configuration: `terraform validate`

**Lambda deployment issues**:
- Check lambda.zip contains all dependencies
- Verify handler path: `wsgi_handler.handler`
- Check CloudWatch logs (if using real AWS)

### Debug Commands

```bash
# Check LocalStack services
curl http://localhost:4566/health

# List Lambda functions
aws --endpoint-url=http://localhost:4566 lambda list-functions

# Invoke function directly
aws --endpoint-url=http://localhost:4566 lambda invoke \
  --function-name library-api \
  --payload '{}' response.json
```

## 📊 Performance Considerations

- **Memory Usage**: Lambda configured for 128MB (adjustable in main.tf)
- **Timeout**: 3 seconds timeout (adjustable in main.tf)
- **Concurrency**: No reserved concurrency set
- **Cold Start**: First request may be slower (~1-2 seconds)

## 🔐 Security Notes

- Uses dummy AWS credentials for LocalStack
- No authentication/authorization implemented (add JWT for production)
- CORS not configured (add flask-cors for web frontends)
- Input validation implemented for all endpoints
- Error messages don't expose sensitive information

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Next Steps

- [ ] Add authentication/authorization
- [ ] Implement database persistence (PostgreSQL/DynamoDB)
- [ ] Add request rate limiting
- [ ] Implement caching (Redis)
- [ ] Add monitoring and logging (CloudWatch/ELK)
- [ ] Create web frontend
- [ ] Add API versioning
- [ ] Implement backup/restore functionality 