#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from ibm_watsonx_ai.wml_client_error import WMLClientError
import time
import warnings


def delete_model_deployment(wml_client, deployment_name: 'str', _silent=True):
    """
    Delete deployment (and model) with name `deployment_name`
    """
    try:
        deployments_details = wml_client.deployments.get_details()
        for deployment in deployments_details['resources']:
            if deployment['entity']['name'] == deployment_name:
                deployment_id = deployment['metadata']['id']
                print('Deleting deployment id', deployment_id)
                wml_client.deployments.delete(deployment_id)
                model_id = deployment['entity']['asset']['id']
                try:
                    print('Deleting model id', model_id)
                    wml_client.repository.delete(model_id)
                except WMLClientError as client_error:
                    print("Could not delete model. Error message:")
                    print(client_error)
            else:
                pass
    except WMLClientError as e:
        if _silent:
            print(f"Not able to delete deployment due to error: {e}")
        else:
            raise e


def bucket_cleanup(cos_resource, prefix='bucket-tests'):
    import datetime
    """
    Delete all buckets started with `prefix`.
    """
    for bucket in cos_resource.buckets.all():
        if bucket.name.startswith(prefix):
            if bucket.creation_date < datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=1):
                try:
                    print(f"Delete bucket older than a days: {bucket.name}")
                    bucket.objects.delete()  # Emptying bucket
                    bucket.delete()  # delete empty bucket
                except Exception as e:
                    print(f"Not able to delete bucket: {bucket.name} due to error: {e}")


def space_cleanup(wml_client, space_id, days_old=1):
    """
    Delete space if older than `days_old`.
    """
    import datetime
    space_details = wml_client.spaces.get_details(space_id)
    creation_date = datetime.datetime.strptime(space_details['metadata'].get('created_at'), "%Y-%m-%dT%H:%M:%S.%fZ")

    if creation_date < datetime.datetime.now() - datetime.timedelta(days=days_old):
        print(f"Delete space {space_details['metadata'].get('name')} {space_details['metadata'].get('guid')} "
              f"older than a days: {days_old}")
        wml_client.set.default_space(space_id)
        deployments = wml_client.deployments.get_details()['resources']
        try:
            for deployment in deployments:
                wml_client.deployments.delete(deployment['metadata']['id'])
            wml_client.spaces.delete(space_id)
        except WMLClientError as e:
            warnings.warn(f"Space cannot be deleted due to the error: {e}")
        time.sleep(10) # wait for space deletion to complete