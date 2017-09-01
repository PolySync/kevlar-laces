#!groovy
node('xenial') {
	stage('Checkout') {
	clean_checkout()
	}
	stage('Test') {
	sh 'cd tests/'
	sh 'behave'
	}
}