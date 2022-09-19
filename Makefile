create_lambda_layer_dependencies:
	rm -rf source/endpoints/__lambda_dependencies__
	pip3 install -r source/endpoints/requirements.txt -t source/endpoints/__lambda_dependencies__  # machine that `cdk deploy` must have same Python version as deployed Lambdas, ie Python 3.9
	rm -rf source/endpoints/__lambda_dependencies__/*.dist-info
