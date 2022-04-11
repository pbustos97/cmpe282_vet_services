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
                    zip archive: true, dir: "UserService/VerifyUser", overwrite: true, zipFile: "${env.ZIP_USER_VERIFY}"

                    echo "SearchService"
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
                        AWS("lambda update-function-code --function-name ${LAMBDA} --s3-bucket ${BUCKET} --s3-key ${env.ZIP_USER_LOGIN} --region ${AWS_DEFAULT_REGION}")
                        AWS("lambda update-function-code --function-name ${LAMBDA2} --s3-bucket ${BUCKET} --s3-key ${env.ZIP_USER_GETROLE} --region ${AWS_DEFAULT_REGION}")
                        AWS("lambda update-function-code --function-name ${LAMBDA3} --s3-bucket ${BUCKET} --s3-key ${env.ZIP_USER_REGISTER} --region ${AWS_DEFAULT_REGION}")
                    }
                }
            }
        }
        // stage("prod-deploy") {
        //     steps {
        //         script {
                    
        //             withCredentials([
        //                 string(credentialsId: 'vet-cicd-bucket', variable: 'BUCKET'), 
        //                 string(credentialsId: 'vet-prod-lambda-create', variable: 'LAMBDA'),
        //                 [
        //                     $class: 'AmazonWebServicesCredentialsBinding',
        //                     credentialsId: "AWS-hootel-prod",
        //                     accessKeyVariable: 'AWS_ACCESS_KEY_ID',
        //                     secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        //                 ]
        //             ]
        //             ) {
        //                 echo "Deploying ${BRANCH_NAME} onto $LAMBDA"
        //                 AWS("s3 cp ${ZIP_LOGINSERVICE} s3://$BUCKET")
        //                 AWS("lambda update-function-code --function-name $LAMBDA --s3-bucket $BUCKET --s3-key ${ZIP_LOGINSERVICE}")
        //         }
        //     }
        // }
    }
}