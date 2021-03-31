import tarfile
import os
import io
import base64
import json
import requests as rt


def list_secrets(t, n, s='http://portainer:9000/api', e= '1'):
    """List swarm secrets.

    List the secrets in a node.

    Args:
        t: Authorization token
        n: Swarm node to make request on
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        List of secrets

    """
    return rt.get(s + '/endpoints/' + e + '/docker/secrets', headers = create_header(t, n)).json()


def create_secret(t, a, b, n='', s='http://portainer:9000/api', e='1'):
    """Create swarm secret.

    Create a docker secret.

    Args:
        t: Authorization token
        b: Path to file containing secret value
        n: Swarm node to make request on
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        ID of created secret

    """
    return rt.post(
        s + '/endpoints/' + e + '/docker/secrets/create',
        headers = create_header(t, n),
        data = get_json(
            {
                'Name': a,
                'Data': base64.b64encode(open(b, 'rb').read()).decode('utf-8')
            }
        )
    ).json()


def get_secret(t, k, n='', s='http://portainer:9000/api', e='1'):
    """Get docker secret.

    Get value of a docker secret.

    Args:
        t: Authorization token
        k: ID of docker secret
        n: Swarm node to make request on
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        Docker secret details

    """
    return rt.get(s + '/endpoints/' + e + '/docker/secrets/' + k, headers = create_header(t, n)).json()


def remove_secret(t, k, n='', s='http://portainer:9000/api', e='1'):
    """Remove docker secret.

    Deletes a docker secret.

    Args:
        t: Authorization token
        k: ID of docker secret
        n: Swarm node to make request on
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        API response

    """
    return rt.delete(s + '/endpoints/' + e + '/docker/secrets/' + k, headers = create_header(t, n))


def get_service_value(v, s, c):
    """Get service value.

    Returns a specified value from a
    given Portainer service.

    Args:
        v: Key for the service value
        s: Portainer service name
        c: Lisf of containers
    Returns:
        Service value.

    """
    return list(map(lambda x: x[v], filter(lambda x: x['service_name'] == s, c)))[0]


def drop_blank_tags(i):
    """Drop blank tags.

    Drops the blank tags from a portainer image list.

    Args:
        i: Portainer image list
    Returns:
        Image list with no blank tags

    """
    return list(filter(lambda x: x['RepoTags'] != None, i))


def get_stack_id(x, y):
    """Get stack id.

    Get the portainer stack id for a given
    stack name.

    Args:
        x: Portainer stack name
        y: Deployed portainer stacks
    Return:
        String portainer stack id

    """
    return str(list(filter(lambda z: z['Name'] == x, y))[0]['Id'])


def create_api_string(x, y):
    """Create the portainer api string.

    Creates the string for connection to the
    portainer api host.

    Args:
        x: Command line arguments (sys.args).
        y: Number of required command line arguments
    Returns:
        The portainer connection string.

    """
    if len(x) - 1 == y:
        return 'http://portainer:9000/api'
    else:
        return 'http://' + x[len(x) -1] + ':9000/api'


def make_tarfile(d):
    """Create a tarfile.

    Create an in-memory byte representation of a .tgz
    file from a folder or file.

    Args:
        d: Path to folder/file to tar
    Returns:
        Byte stream of tar archive

    """
    t = io.BytesIO()
    with tarfile.open(fileobj=t, mode="w:gz") as tar:
        tar.add(d, arcname=os.path.basename(d))
    t.seek(0)
    return t


def get_dict(x):
    """Convert JSON to Python dict.

    Convert a JSON String into a Python dictionary.

    Args:
        x: JSON String
    Returns:
        Python dictionary

    """
    return json.loads(x)


def get_json(x):
    """Convert Python dict to JSON.

    Convert Python dictionary into a JSON string.

    Args:
        x: Python dictionary
    Returns:
        JSON string

    """
    return json.dumps(x)


def initialize_admin_account(p, s= 'http://portainer:9000/api'):
    """Set portainer admin password.

    Sets the portainer admin password.

    Args:
        p: Password
        s: Portainer server api endpoint
    Returns:
        API response

    """
    return rt.post(s + '/users/admin/init', data = get_json({'Username': 'admin', 'Password': p}))


def generate_token(u, p, s='http://portainer:9000/api'):
    """Generate portainer token.

    Generate a token for using Portainer api.
    A token lasts 8 hours.

    Args:
        u: Username
        p: Password
        s: Portainer server api endpoint
    Returns:
        Portainer token

    """
    return rt.post(s + '/auth', data = get_json({'Username': u, 'Password': p})).json()['jwt']


def create_header(t, n='', tar=False):
    """Create header for API request.

    Args:
        t: Authorization token
        n: Swarm node to make request on
    Returns:
        Request header in JSON

    """
    if not tar:
        return({'Authorization': 'Bearer ' + t, 'X-PortainerAgent-Target': n, 'Content-Type': 'application/json'})
    else:
        return({'Authorization': 'Bearer ' + t, 'X-PortainerAgent-Target': n, 'Content-Type': 'application/x-tar'})


def list_images(t, n='', s='http://portainer:9000/api', e='1'):
    """List swarm containers.

    List the images on a node.

    Args:
        t: Authorization token
        n: Swarm node to make request on
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        List of image details

    """
    return rt.get(s + '/endpoints/' + e + '/docker/images/json', headers = create_header(t, n)).json()


def get_image(i, t, n='', s='http://portainer:9000/api', e='1'):
    """Get swarm id.

    Get the swarm id needed for deploying stacks.

    Args:
        i: Image id
        t: Authorization token
        n: Swarm node name
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        Details of docker image

    """
    return rt.get(s + '/endpoints/' + e + '/docker/images/' + i + '/json', headers = create_header(t, n)).json()


def list_services(t, s='http://portainer:9000/api', e='1') :
    """List swarm services.

    List the services on the swarm.

    Args:
        t: Authorization token
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        List of sevice details

    """
    return rt.get(s + '/endpoints/' + e + '/docker/services', headers = create_header(t)).json()


def list_containers(t, n='', s='http://portainer:9000/api', e='1'):
    """List swarm containers.

    List the container on the swarm.

    Args:
        t: Authorization token
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        List of container details

    """
    return rt.get(s + '/endpoints/' + e + '/docker/containers/json', headers = create_header(t, n)).json()


def get_container_volumes(c):
    """Extract volume names.

    Extracts the volume names for a container.

    Args:
        c: Container dictionary from portainer api
    Returns:
        List of attached volume names

    """
    return list(map(lambda x: x['Name'], filter(lambda x: x['Type'] == 'volume', c['Mounts'])))


def get_container_details(c):
    """Create container summary.

    Create a summary of a container. Ignores swarm labels
    for non service containers.

    Args:
        c: Container dictionary from portainer api
    Returns:
        Dictionary with container summary

    """
    d = dict()
    d['id'] = c['Id']
    if 'com.docker.stack.namespace' in c['Labels']:
        d['stack_name'] = c['Labels']['com.docker.stack.namespace']
        d['service_id'] = c['Labels']['com.docker.swarm.service.id']
        d['service_name'] = c['Labels']['com.docker.swarm.service.name']
        d['node_id'] = c['Labels']['com.docker.swarm.node.id']
        d['node_name'] = c['Portainer']['Agent']['NodeName']
        d['task_id'] = c['Labels']['com.docker.swarm.task.id']
        d['task_name'] = c['Labels']['com.docker.swarm.task.name']
    else:
        d['stack_name'] = "NA"
        d['service_id'] = c['Labels']['com.docker.swarm.service.id']
        d['service_name'] = c['Labels']['com.docker.swarm.service.name']
        d['node_id'] = c['Labels']['com.docker.swarm.node.id']
        d['node_name'] = c['Portainer']['Agent']['NodeName']
        d['task_id'] = c['Labels']['com.docker.swarm.task.id']
        d['task_name'] = c['Labels']['com.docker.swarm.task.name']
    d['volumes'] = get_container_volumes(c)
    return d


def get_container_summary(c):
    """Summarize swarm container output.

    Produces a summerized version of the container list.

    Args:
        c: List of portainer api container output
    Returns:
        List of container summaries

    """
    return list(map(get_container_details, c))


def exec_container(c, d, t, n, s='http://portainer:9000/api', e='1'):
    """Execute command within container.

    Execute a command within a running container.

    Args:
        c: Container id
        d: List containing command
        t: Authorization token
        n: Container swarm node
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        Portainer api response

    """
    endpoint = s + '/endpoints/' + e + '/docker'
    data = get_json({'AttachStdin': False,'AttachStdout': True,'AttachStderr': True, 'Tty': False, 'Cmd': d})
    start_data = '{"Detach": false, "Tty": false}'
    job = rt.post(endpoint +'/containers/' + c + '/exec', headers = create_header(t, n), data = data).json()['Id']
    return rt.post(endpoint + '/exec/' + job + '/start',  headers = create_header(t, n), data = start_data)


def get_id_from_name(x, y):
    """Get id from api search results.

    Get the id for a given name.

    Args:
        x: Portainer name
        y: List of results
    Return:
        String portainer id

    """
    return str(list(filter(lambda z: z['Name'] == x, y))[0]['Id'])


def get_endpoint_id(t, n='primary', s='http://portainer:9000/api'):
    """Get endpoint id.

    Get the portainer endpoint id.

    Args:
        t: Authorization token
        n: Docker endpoint name
        s: Portainer server api endpoint
    Returns:
        Swarm id string

    """
    endpoints = rt.get(s + '/endpoints', headers = create_header(t)).json()
    return get_id_from_name(n, endpoints)


def get_swarm_id(t, s='http://portainer:9000/api', e='1'):
    """Get swarm id.

    Get the swarm id needed for deploying stacks.

    Args:
        t: Authorization token
        e: Docker endpoint id
        s: Portainer server api endpoint
    Returns:
        Swarm id string

    """
    return rt.get(s + '/endpoints/' + e + '/docker/swarm', headers = create_header(t)).json()['ID']


def add_to_container(c, n, t, p, f, s='http://portainer:9000/api', e='1'):
    """Add files to running container.

    Adds a .tgz archive to a running container.

    Args:
        c: Container id
        n: Swarm node name
        t: Authorization token
        p: Path in container to put files
        f: Path to host folder to create .tgz archive from
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        Portainer api response

    """
    return rt.put(
        s + '/endpoints/' + e + '/docker/containers/' + c + '/archive',
        headers = create_header(t, n, True),
        params = {'path': p},
        data = make_tarfile(f)
    )


def pull_image(i, t, n='', s='http://portainer:9000/api', e='1'):
    """Pull docker image.

    Pull an image from Dockerhub or from a private registry.
    Private registeries need to be defined within Portainer.

    Args:
        i: Image to pull
        t: Authorization token
        n: Swarm node name
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        Portainer api response

    """
    return rt.post(
        s + '/endpoints/' + e + '/docker/images/create',
        headers = create_header(t, n),
        params = {'fromImage': i}
    )


def push_image(i, t, u='', p='', r='docker.service:5000', n='', s='http://portainer:9000/api', e='1'):
    """Push docker image to repository.

    Push an image to Dockerhub or a private registry.
    Leaving username and password blank will use an unsecured repo.
    Private registeries need to be defined within Portainer.

    Args:
        i: Image name to push
        t: Authorization token
        u: registry username
        p: registry password
        n: Swarm node name
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        Portainer api response

    """
    return rt.post(
        s + '/endpoints/' + e + '/docker/images/' + i + '/push',
        headers = {
            'Authorization': 'Bearer ' + t,
            'X-Registry-Auth': base64.b64encode(
                b'{"username": "'+ bytes(u, 'utf-8') +
                b'", "password": "' + bytes(p, 'utf-8') +
                b'", "serveraddress": "' + bytes(r, 'utf-8') + b'"}'
            ),
            'X-PortainerAgent-Target': n
        }
    )


def build_image(n, t, p, d= 'Dockerfile', s='http://portainer:9000/api', e='1'):
    """Build docker image.

    Build a docker image from a .tgz archive build context.

    Args:
        n: Swarm node name for build
        t: Authorization token
        p: Dictionary of build parameters
        d: .tgz archive of folder containing the build context
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        Portainer api response

    """
    return rt.post(s + '/endpoints/' + e + '/docker/build', headers = create_header(t, n, True), params = p, data = make_tarfile(d))


def tag_image(t, i, r, n='', s='http://portainer:9000/api', e='1'):
    """Tag image.

    Add a new tag to a Docker image.

    Args:
        t: Authorization token
        i: Image id
        r: New tag
        n: Swarm node name
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        Portainer api response

    """
    return rt.post(
        s + '/endpoints/' + e + '/docker/images/' + i + '/tag',
        headers = create_header(t, n), params = {'repo': r}
    )


def list_stacks(t, s='http://portainer:9000/api', e='1'):
    """List swarm stacks.

    List swarm stacks deployed via Portainer api.

    Args:
        t: Authorization token
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        List of stack objects

    """
    return rt.get(s +'/stacks', headers = create_header(t)).json()


def deploy_stack(w, t, n, d, y='1', s='http://portainer:9000/api', e='1'):
    """Deploy swarm stack.

    Deploy a swarm stack with the Portainer api.

    Args:
        w: Swarm id
        t: Authorization token
        n: Stack name
        d: Path to docker-compose
        y: Deployment type 1 (Swarm) 2 (Compose)
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        Portainer api response

    """
    params = {'type': y, 'method': 'string', 'endpointId': e}
    data = {'SwarmID': w, 'Name': n, 'StackFileContent': open(d, 'r').read()}
    return rt.post(s +'/stacks', headers = create_header(t), params = params, data = get_json(data))


def remove_stack(w, t, s='http://portainer:9000/api', e='1'):
    """Remove swarm stack.

    Remove a swarm stack via the Portainer api.

    Args:
        w: Stack id
        t: Authorization token
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        Portainer api response

    """
    return rt.delete(s + '/stacks/' + w, headers = create_header(t), params = {'endpointId': e})


def print_api_output(a):
    """Print portainer api output.

    Prints the output from the portainer api
    replacing greater than signs.

    Args:
        a: Portainer api response
    Returns:
        Boolean true

    """
    output = a.text.replace(r'\u003e', ">")
    list_out = [x for x in output.split('\r\n')]
    for y in list_out:
        print(y)
    return True


def list_nodes(t, s='http://portainer:9000/api', e='1'):
    """List swarm nodes.

    List the nodes on the swarm.

    Args:
        t: Authorization token
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        List of sevice details

    """
    return rt.get(s + '/endpoints/' + e + '/docker/nodes', headers = create_header(t)).json()


def get_node(t, n, s='http://portainer:9000/api', e='1'):
    """List swarm nodes.

    List the nodes on the swarm.

    Args:
        t: Authorization token
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        List of sevice details

    """
    return rt.get(s + '/endpoints/' + e + '/docker/nodes/' + n , headers = create_header(t)).json()


def describe_swarm(t, s='http://portainer:9000/api', e='1'):
    """List swarm nodes.

    List the nodes on the swarm.

    Args:
        t: Authorization token
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        List of sevice details

    """
    return rt.get(s + '/endpoints/' + e + '/docker/swarm', headers = create_header(t)).json()


def get_labels(t, n, s='http://portainer:9000/api', e='1'):
    """Deploy swarm stack.

    Deploy a swarm stack with the Portainer api.

    Args:
        w: Swarm id
        t: Authorization token
        n: Stack name
        d: Path to docker-compose
        y: Deployment type 1 (Swarm) 2 (Compose)
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        Portainer api response

    """
    return rt.get(
	s +'/endpoints/' + e + '/docker/nodes/' + n,
	headers = create_header(t)
    ).json()["Spec"]["Labels"]


def add_label(w, t, n, s='http://portainer:9000/api', e='1'):
    """Deploy swarm stack.

    Deploy a swarm stack with the Portainer api.

    Args:
        w: Swarm id
        t: Authorization token
        n: Stack name
        d: Path to docker-compose
        y: Deployment type 1 (Swarm) 2 (Compose)
        s: Portainer server api endpoint
        e: Docker endpoint id
    Returns:
        Portainer api response

    """

    labels = get_labels(t, n, s, e)
    labels[w] = 'True'

    data = {'Availability': 'active', 'Role': 'worker', 'Labels': labels}
    return rt.post(
	s +'/endpoints/' + e + '/docker/nodes/' + n + '/update',
	headers = create_header(t),
	params = {'version': get_node(t, n, s, e)['Version']['Index']},
	data = get_json(data)
    )

