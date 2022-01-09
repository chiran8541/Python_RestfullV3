 pipeline {
   agent any
    parameters {
		string(description: 'ScriptfileName', name: 'ScriptfileName')
    }
    stages {
			stage('Executing the script in develop') {
                 when {
                   branch 'develop'
               }
               steps {
                script {
                  		sh """
							   mkdir -p /tmp/buckets
                            cp ${workspace}/AWS-CLI/$ScriptfileName /tmp/buckets
							cd /tmp/buckets
                            aws configure set default.region us-east-1
							chmod 755 $ScriptfileName
							./$ScriptfileName
							rm -f $ScriptfileName
                               """
                        }

                    }
                }
			
    }	
	}
