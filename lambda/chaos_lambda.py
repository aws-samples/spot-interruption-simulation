import os
import boto3
import random
import time

# ENV VARs
SIMULATION_STEP_FN_ARN = os.environ['SIMULATION_STEP_FN_ARN']

FIS_TEMPLATES_ASG = ['Spot_ASG_FIS_Experiment_Template_1','Spot_ASG_FIS_Experiment_Template_2']

__author__ = "ssengott@"
#chaos lamdba to simulate spot interruption. to be called in schedule. say, every 5 mins.
def lambda_handler(event, context):

    print("chaos lambda. invoke simulation step function")
    print(event)

    try:
        fis_client = boto3.client('fis')
        # interrupt spot instance
        interrupt_spot_instance(fis_client, FIS_TEMPLATES_ASG)

        # invoke step function
        # call step function to invoke simulation /availability check
        client = boto3.client('stepfunctions')
        response = client.start_execution(stateMachineArn=SIMULATION_STEP_FN_ARN)
        print("invoked step function for simulation /availability check.")
    except Exception as ex:
        print("Exception in interruption/step function execution. Exception=:" + str(ex))

    print("completed chaos for this schedule")


#function to simulate spot eviction with FIS
def interrupt_spot_instance(fis_client, FIS_TEMPLATES):
    start = time.time()
    fis_exp_templates = fis_client.list_experiment_templates()
    exp_templates = fis_exp_templates['experimentTemplates']
    # print(fis_exp_templates['experimentTemplates'])

    RANDOM_FIS_TEMPLATE = random.choice(FIS_TEMPLATES)
    print("selected FIS template="+RANDOM_FIS_TEMPLATE)

    for exp_template in exp_templates:
        if RANDOM_FIS_TEMPLATE == exp_template['description']:
            # exception handling.  continue even if it fails for one team.
            try:
                exp_id = exp_template['id']
                print(exp_template['description'])
                print(exp_id)
                print("starting experiment....")
                exp_response = fis_client.start_experiment(experimentTemplateId=exp_id)
                exp = exp_response['experiment']
                print("experiment id=" + exp['id'])
                print('experiment status=' + exp['state']['status'])
                print('experiment spot eviction action status=' + exp['actions']['SpotEvection']['state']['status'])
            except Exception as excp:
                print("GD: Exception in running Experiment:" + str(excp))
            break

    print(f"Runtime of interrupt_spot_instance is: {time.time() - start}")