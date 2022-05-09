@Library('github.com/releaseworks/jenkinslib') _

pipeline {

    // Where to execute the pipeline script
    agent any

    environment{
        AWS_DEFAULT_REGION="us-west-2"
        AWS_CREDENTIALS=credentials('AWS-hootel-dev')
        ZIP_USER_LOGIN="Vet-UserService-Login.zip"
        ZIP_USER_REGISTER="Vet-UserService-Register.zip"
        ZIP_USER_GETROLE="Vet-UserService-GetRole.zip"
        ZIP_USER_UPDATE="Vet-UserService-Update.zip"
        ZIP_DOC_REGISTER="Vet-DocService-Register.zip"
        ZIP_DOC_GET="Vet-DocService-GetDoc.zip"
        ZIP_PET_REGISTER="Vet-PetService-Register.zip"
        ZIP_PET_GET="Vet-PetService-GetPet.zip"
    }

    // Different pipeline stages
    stages {
        stage("init") {
            steps {
                script {
                    echo "Initializing Pipeline"
                }
            }
        }

        // Zips up the folders
        stage("build") {
            steps {
                script {
                    echo "Building ${BRANCH_NAME}"

                    echo "UserService"
                    zip archive: true, dir: "UserService/Login", overwrite: true, zipFile: "${env.ZIP_USER_LOGIN}"
                    zip archive: true, dir: "UserService/GetRole", overwrite: true, zipFile: "${env.ZIP_USER_GETROLE}"
                    zip archive: true, dir: "UserService/Register", overwrite: true, zipFile: "${env.ZIP_USER_REGISTER}"
                    zip archive: true, dir: "UserService/Update", overwrite: true, zipFile: "${env.ZIP_USER_UPDATE}"
                    echo "DoctorService"
                    zip archive: true, dir: "DoctorService/DoctorRegister", overwrite: true, zipFile: "${env.ZIP_DOC_REGISTER}"
                    zip archive: true, dir: "DoctorService/DoctorGet", overwrite: true, zipFile: "${env.ZIP_DOC_GET}"
                    echo "PetService"
                    zip archive: true, dir: "PetService/RegisterPet", overwrite: true, zipFile: "${env.ZIP_PET_REGISTER}"
                    zip archive: true, dir: "PetService/GetPet", overwrite: true, zipFile: "${env.ZIP_PET_GET}"
                    echo "Misc"
                }
            }
        }

        // Uploads zipped folders to Lambda directly if under 10MB
        stage("dev-deploy") {
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'vet-cicd-bucket', variable: 'BUCKET'), 
                        string(credentialsId: 'vet-dev-lambda-UserLogin', variable: 'LAMBDA'),
                        string(credentialsId: 'vet-dev-lambda-UserGetRole', variable: 'LAMBDA2'),
                        string(credentialsId: 'vet-dev-lambda-UserRegister', variable: 'LAMBDA3'),
                        string(credentialsId: 'vet-dev-lambda-DocGet', variable: 'LAMBDA4'),
                        string(credentialsId: 'vet-dev-lambda-DocRegister', variable: 'LAMBDA5'),
                        string(credentialsId: 'vet-dev-lambda-PetGet', variable: 'LAMBDA6'),
                        string(credentialsId: 'vet-dev-lambda-PetRegister', variable: 'LAMBDA7'),
                        [
                            $class: 'AmazonWebServicesCredentialsBinding',
                            credentialsId: "AWS-hootel-dev",
                            accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                            secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                        ]
                    ]
                    ) {
                        echo "Deploying ${BRANCH_NAME} onto ${LAMBDA}"
                        AWS("s3 cp ${env.ZIP_USER_LOGIN} s3://${BUCKET}")
                        AWS("s3 cp ${env.ZIP_USER_GETROLE} s3://${BUCKET}")
                        AWS("s3 cp ${env.ZIP_USER_REGISTER} s3://${BUCKET}")
                        AWS("s3 cp ${env.ZIP_DOC_GET} s3://${BUCKET}")
                        AWS("s3 cp ${env.ZIP_DOC_REGISTER} s3://${BUCKET}")
                        AWS("s3 cp ${env.ZIP_PET_GET} s3://${BUCKET}")
                        AWS("s3 cp ${env.ZIP_PET_REGISTER} s3://${BUCKET}")
                        AWS("lambda update-function-code --function-name ${LAMBDA} --s3-bucket ${BUCKET} --s3-key ${env.ZIP_USER_LOGIN} --region ${AWS_DEFAULT_REGION}")
                        AWS("lambda update-function-code --function-name ${LAMBDA2} --s3-bucket ${BUCKET} --s3-key ${env.ZIP_USER_GETROLE} --region ${AWS_DEFAULT_REGION}")
                        AWS("lambda update-function-code --function-name ${LAMBDA3} --s3-bucket ${BUCKET} --s3-key ${env.ZIP_USER_REGISTER} --region ${AWS_DEFAULT_REGION}")
                        AWS("lambda update-function-code --function-name ${LAMBDA4} --s3-bucket ${BUCKET} --s3-key ${env.ZIP_DOC_GET} --region ${AWS_DEFAULT_REGION}")
                        AWS("lambda update-function-code --function-name ${LAMBDA5} --s3-bucket ${BUCKET} --s3-key ${env.ZIP_DOC_REGISTER} --region ${AWS_DEFAULT_REGION}")
                        AWS("lambda update-function-code --function-name ${LAMBDA6} --s3-bucket ${BUCKET} --s3-key ${env.ZIP_PET_GET} --region ${AWS_DEFAULT_REGION}")
                        AWS("lambda update-function-code --function-name ${LAMBDA7} --s3-bucket ${BUCKET} --s3-key ${env.ZIP_PET_REGISTER} --region ${AWS_DEFAULT_REGION}")
                    }
                }
            }
        }
    }
}