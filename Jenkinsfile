#!groovy
node('four') {
	stage('Checkout') {
	  clean_checkout()
	}
	stage('Test') {
    sh 'gpg2 --version'
	  sh 'behave -v -x --capture'
	}
}
