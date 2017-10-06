#!groovy
node('xenial') {
	stage('Checkout') {
	  clean_checkout()
	}
	stage('Test') {
	  sh 'cd tests && behave -v -x --capture'
	}
}
