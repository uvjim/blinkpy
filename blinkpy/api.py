"""Implements known blink API calls."""

import logging
import string
import time
import random
from json import dumps
from blinkpy.helpers.util import get_time, Throttle
from blinkpy.helpers.constants import DEFAULT_URL, TIMEOUT, DEFAULT_USER_AGENT

_LOGGER = logging.getLogger(__name__)

MIN_THROTTLE_TIME = 5


def request_login(
    auth,
    url,
    login_data,
    is_retry=False,
):
    """
    Login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    """
    headers = {
        "Host": DEFAULT_URL,
        "Content-Type": "application/json",
        "user-agent": DEFAULT_USER_AGENT,
    }
    data = dumps(
        {
            "email": login_data["username"],
            "password": login_data["password"],
            "unique_id": login_data["uid"],
            "device_identifier": login_data["device_id"],
            "client_name": "Computer",
            "reauth": True,
        }
    )

    return auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
    )


def request_verify(auth, blink, verify_key):
    """Send verification key to blink servers."""
    url = f"{blink.urls.base_url}/api/v4/account/{blink.account_id}/client/{blink.client_id}/pin/verify"
    data = dumps({"pin": verify_key})
    return auth.query(
        url=url,
        headers=auth.header,
        data=data,
        json_resp=False,
        reqtype="post",
    )


def request_logout(blink):
    """Logout of blink servers."""
    url = f"{blink.urls.base_url}/api/v4/account/{blink.account_id}/client/{blink.client_id}/logout"
    return http_post(blink, url=url)


def request_networks(blink):
    """Request all networks information."""
    url = f"{blink.urls.base_url}/networks"
    return http_get(blink, url)


def request_network_update(blink, network):
    """
    Request network update.

    :param blink: Blink instance.
    :param network: Sync module network id.
    """
    url = f"{blink.urls.base_url}/network/{network}/update"
    return http_post(blink, url)


def request_user(blink):
    """Get user information from blink servers."""
    url = f"{blink.urls.base_url}/user"
    return http_get(blink, url)


def request_network_status(blink, network):
    """
    Request network information.

    :param blink: Blink instance.
    :param network: Sync module network id.
    """
    url = f"{blink.urls.base_url}/network/{network}"
    return http_get(blink, url)


def request_syncmodule(blink, network):
    """
    Request sync module info.

    :param blink: Blink instance.
    :param network: Sync module network id.
    """
    url = f"{blink.urls.base_url}/network/{network}/syncmodules"
    return http_get(blink, url)


@Throttle(seconds=MIN_THROTTLE_TIME)
def request_system_arm(blink, network):
    """
    Arm system.

    :param blink: Blink instance.
    :param network: Sync module network id.
    """
    url = f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}/networks/{network}/state/arm"
    return http_post(blink, url)


@Throttle(seconds=MIN_THROTTLE_TIME)
def request_system_disarm(blink, network):
    """
    Disarm system.

    :param blink: Blink instance.
    :param network: Sync module network id.
    """
    url = f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}/networks/{network}/state/disarm"
    return http_post(blink, url)


def request_command_status(blink, network, command_id):
    """
    Request command status.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param command_id: Command id to check.
    """
    url = f"{blink.urls.base_url}/network/{network}/command/{command_id}"
    return http_get(blink, url)


@Throttle(seconds=MIN_THROTTLE_TIME)
def request_homescreen(blink):
    """Request homescreen info."""
    url = f"{blink.urls.base_url}/api/v3/accounts/{blink.account_id}/homescreen"
    return http_get(blink, url)


@Throttle(seconds=MIN_THROTTLE_TIME)
def request_sync_events(blink, network):
    """
    Request events from sync module.

    :param blink: Blink instance.
    :param network: Sync module network id.
    """
    url = f"{blink.urls.base_url}/events/network/{network}"
    return http_get(blink, url)


@Throttle(seconds=MIN_THROTTLE_TIME)
def request_new_image(blink, network, camera_id):
    """
    Request to capture new thumbnail for camera.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: Camera ID of camera to request new image from.
    """
    url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/thumbnail"
    return http_post(blink, url)


@Throttle(seconds=MIN_THROTTLE_TIME)
def request_new_video(blink, network, camera_id):
    """
    Request to capture new video clip.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: Camera ID of camera to request new video from.
    """
    url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/clip"
    return http_post(blink, url)


@Throttle(seconds=MIN_THROTTLE_TIME)
def request_video_count(blink):
    """Request total video count."""
    url = f"{blink.urls.base_url}/api/v2/videos/count"
    return http_get(blink, url)


def request_videos(blink, time=None, page=0):
    """
    Perform a request for videos.

    :param blink: Blink instance.
    :param time: Get videos since this time.  In epoch seconds.
    :param page: Page number to get videos from.
    """
    timestamp = get_time(time)
    url = f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}/media/changed?since={timestamp}&page={page}"
    return http_get(blink, url)


def request_cameras(blink, network):
    """
    Request all camera information.

    :param Blink: Blink instance.
    :param network: Sync module network id.
    """
    url = f"{blink.urls.base_url}/network/{network}/cameras"
    return http_get(blink, url)


def request_camera_info(blink, network, camera_id):
    """
    Request camera info for one camera.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: Camera ID of camera to request info from.
    """
    url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/config"
    return http_get(blink, url)


def request_camera_usage(blink):
    """
    Request camera status.

    :param blink: Blink instance.
    """
    url = f"{blink.urls.base_url}/api/v1/camera/usage"
    return http_get(blink, url)


def request_camera_liveview(blink, network, camera_id):
    """
    Request camera liveview.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: Camera ID of camera to request liveview from.
    """
    url = f"{blink.urls.base_url}/api/v5/accounts/{blink.account_id}/networks/{network}/cameras/{camera_id}/liveview"
    return http_post(blink, url)


def request_camera_sensors(blink, network, camera_id):
    """
    Request camera sensor info for one camera.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: Camera ID of camera to request sesnor info from.
    """
    url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/signals"
    return http_get(blink, url)


@Throttle(seconds=MIN_THROTTLE_TIME)
def request_motion_detection_enable(blink, network, camera_id):
    """
    Enable motion detection for a camera.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: Camera ID of camera to enable.
    """
    url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/enable"
    return http_post(blink, url)


@Throttle(seconds=MIN_THROTTLE_TIME)
def request_motion_detection_disable(blink, network, camera_id):
    """Disable motion detection for a camera.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: Camera ID of camera to disable.
    """
    url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/disable"
    return http_post(blink, url)


def request_local_storage_manifest(blink, network, sync_id, max_retries=10):
    """Request creation of an updated manifest of video clips stored in sync module local storage.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param sync_id: ID of sync module.
    :param max_retries: Number of polling retries.
    """
    url = (
        f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}/networks/{network}/sync_modules/{sync_id}"
        + "/local_storage/manifest/request"
    )

    # The sync module may be busy processing another request (like saving a new clip).
    # Poll the endpoint until it is ready, backing off each retry.
    response = None
    time.sleep(1)
    retry = 0
    while True:
        if retry > max_retries:
            break
        response = http_post(blink, url)
        if "id" in response:
            break
        seconds = backoff_seconds(retry=retry, default_time=3)
        _LOGGER.debug("Retrying in %d seconds: %s", seconds, url)
        time.sleep(seconds)
        retry += 1
    return response


def get_local_storage_manifest(
    blink, network, sync_id, manifest_request_id, max_retries=8
):
    """Request manifest of video clips stored in sync module local storage.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param sync_id: ID of sync module.
    :param manifest_request_id: Request ID of local storage manifest (requested creation of new manifest).
    :param max_retries: Number of polling retries.
    """
    url = (
        f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}/networks/{network}/sync_modules/{sync_id}"
        + f"/local_storage/manifest/request/{manifest_request_id}"
    )
    # It takes some time for the sync module to build the manifest (if the sync module is busy).
    # Poll the endpoint until it is ready, backing off each retry.
    response = None
    time.sleep(1)
    retry = 0
    while True:
        if retry > max_retries:
            break
        response = http_get(blink, url)
        if "clips" in response:
            break
        seconds = backoff_seconds(retry=retry)
        _LOGGER.debug("Retrying in %d seconds: %s", seconds, url)
        time.sleep(seconds)
        retry += 1
    return response


def request_local_storage_clip(
    blink, network, sync_id, manifest_id, clip_id, max_retries=5
):
    """Prepare video clip stored in the sync module to be downloaded.

    :param blink:
    :param network:
    :param sync_id:
    :param manifest_id:
    :param clip_id:
    :param max_retries:
    :return:
    """
    url = blink.urls.base_url + string.Template(
        local_storage_clip_url_template()
    ).substitute(
        account_id=blink.account_id,
        network_id=network,
        sync_id=sync_id,
        manifest_id=manifest_id,
        clip_id=clip_id,
    )
    return http_post(blink, url)


def local_storage_clip_url_template():
    """Return URL template for local storage clip download location."""
    return (
        "/api/v1/accounts/$account_id/networks/$network_id/sync_modules/$sync_id"
        "/local_storage/manifest/$manifest_id/clip/request/$clip_id"
    )


def http_get(blink, url, stream=False, json=True, is_retry=False, timeout=TIMEOUT):
    """Perform an http get request.

    :param url: URL to perform get request.
    :param stream: Stream response? True/FALSE
    :param json: Return json response? TRUE/False
    :param is_retry: Is this part of a re-auth attempt?
    """
    _LOGGER.debug("Making GET request to %s", url)
    return blink.auth.query(
        url=url,
        headers=blink.auth.header,
        reqtype="get",
        stream=stream,
        json_resp=json,
        is_retry=is_retry,
    )


def http_post(blink, url, is_retry=False, data=None, json=True, timeout=TIMEOUT):
    """Perform an http post request.

    :param url: URL to perfom post request.
    :param is_retry: Is this part of a re-auth attempt?
    :param data: str body for post request
    :param json: Return json response? TRUE/False
    """
    _LOGGER.debug("Making POST request to %s", url)
    return blink.auth.query(
        url=url,
        headers=blink.auth.header,
        reqtype="post",
        is_retry=is_retry,
        json_resp=json,
        data=data,
    )


def backoff_seconds(retry=0, default_time=1):
    """Calculate number of seconds to back off for retry."""
    return default_time * 2**retry + random.uniform(0, 1)
