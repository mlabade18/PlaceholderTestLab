pipeline {
    agent any
    
    parameters {
        choice(
            name: 'DB_TYPE',
            choices: ['sqlite', 'postgresql', 'mysql'],
            description: 'Select Database Type'
        )
        choice(
            name: 'TEST_LEVEL',
            choices: ['smoke', 'regression', 'all'],
            description: 'Select Test Level'
        )
        booleanParam(
            name: 'GENERATE_REPORT',
            defaultValue: true,
            description: 'Generate HTML Report'
        )
        choice(
            name: 'PARALLEL_WORKERS',
            choices: ['1', '2', '4', '8', 'auto'],
            description: 'Number of Parallel Workers (auto = CPU count)'
        )
    }
    
    environment {
        PYTHON_VERSION = '3.8'
        PROJECT_PATH = '/Users/madhurilabade/PIP Project 1/PlaceholderTestLab'
        VENV_PATH = '${PROJECT_PATH}/venv'
        DB_TYPE = "${params.DB_TYPE}"
        LOG_LEVEL = 'INFO'
        PARALLEL_WORKERS = "${params.PARALLEL_WORKERS}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "========== Checking out code =========="
                    checkout scm
                }
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    echo "========== Setting up Python environment =========="
                    sh '''
                        cd "${PROJECT_PATH}"
                        
                        # Create virtual environment if not exists
                        if [ ! -d "venv" ]; then
                            python3 -m venv venv
                        fi
                        
                        # Activate virtual environment
                        . venv/bin/activate
                        
                        # Upgrade pip
                        pip install --upgrade pip
                        
                        # Install dependencies
                        pip install -r requirements.txt
                        
                        echo "Environment setup completed"
                    '''
                }
            }
        }
        
        stage('Database Setup') {
            steps {
                script {
                    echo "========== Setting up ${DB_TYPE} database =========="
                    sh '''
                        cd "${PROJECT_PATH}"
                        . venv/bin/activate
                        
                        if [ "${DB_TYPE}" = "postgresql" ]; then
                            echo "Installing PostgreSQL dependencies"
                            pip install psycopg2-binary
                        elif [ "${DB_TYPE}" = "mysql" ]; then
                            echo "Installing MySQL dependencies"
                            pip install mysql-connector-python
                        fi
                    '''
                }
            }
        }
        
        stage('Code Quality Check') {
            steps {
                script {
                    echo "========== Running Code Quality Checks =========="
                    sh '''
                        cd "${PROJECT_PATH}"
                        . venv/bin/activate
                        
                        # Run pylint
                        pylint src/ --exit-zero || true
                        
                        # Run flake8
                        flake8 src/ tests/ --max-line-length=120 || true
                        
                        echo "Code quality checks completed"
                    '''
                }
            }
        }
        
        stage('Run Tests (Parallel)') {
            steps {
                script {
                    echo "========== Running Tests in Parallel =========="
                    sh '''
                        cd "${PROJECT_PATH}"
                        . venv/bin/activate
                        
                        # Determine worker count
                        if [ "${PARALLEL_WORKERS}" = "auto" ]; then
                            WORKERS=$(python3 -c "import os; print(os.cpu_count())")
                        else
                            WORKERS="${PARALLEL_WORKERS}"
                        fi
                        
                        echo "Using ${WORKERS} parallel workers"
                        
                        if [ "${TEST_LEVEL}" = "smoke" ]; then
                            pytest tests/ -m smoke -v --tb=short -n ${WORKERS} \
                                --dist=loadscope
                        elif [ "${TEST_LEVEL}" = "regression" ]; then
                            pytest tests/ -m regression -v --tb=short -n ${WORKERS} \
                                --dist=loadscope
                        else
                            pytest tests/ -v --tb=short -n ${WORKERS} \
                                --dist=loadscope
                        fi
                    '''
                }
            }
        }
        
        stage('Generate Report') {
            when {
                expression { params.GENERATE_REPORT == true }
            }
            steps {
                script {
                    echo "========== Generating Test Reports =========="
                    sh '''
                        cd "${PROJECT_PATH}"
                        . venv/bin/activate
                        
                        # Generate HTML report
                        pytest tests/ -v \
                            --html=reports/report.html \
                            --self-contained-html \
                            --cov=src \
                            --cov-report=html:reports/coverage \
                            || true
                        
                        echo "Reports generated in reports/ directory"
                    '''
                }
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                script {
                    echo "========== Archiving Test Artifacts =========="
                    sh '''
                        cd "${PROJECT_PATH}"
                        
                        # Create logs directory if needed
                        mkdir -p logs reports
                    '''
                    
                    archiveArtifacts artifacts: 'logs/**/*.log,reports/**/*', 
                                     allowEmptyArchive: true
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "========== Cleaning up =========="
                sh '''
                    cd "${PROJECT_PATH}"
                    
                    # Generate summary
                    echo "Test execution completed at $(date)" >> logs/pipeline_summary.log
                    echo "Database Type: ${DB_TYPE}" >> logs/pipeline_summary.log
                    echo "Test Level: ${TEST_LEVEL}" >> logs/pipeline_summary.log
                    echo "Parallel Workers: ${PARALLEL_WORKERS}" >> logs/pipeline_summary.log
                '''
            }
        }
        
        success {
            script {
                echo "========== Pipeline Successful =========="
                // Send notification on success (optional)
                // emailext(
                //     subject: 'Test Pipeline Successful',
                //     body: 'All tests passed successfully',
                //     to: 'your-email@example.com'
                // )
            }
        }
        
        failure {
            script {
                echo "========== Pipeline Failed =========="
                // Send notification on failure (optional)
                // emailext(
                //     subject: 'Test Pipeline Failed',
                //     body: 'Some tests failed. Check Jenkins for details',
                //     to: 'your-email@example.com'
                // )
            }
        }
        
        cleanup {
            cleanWs()
        }
    }
}
