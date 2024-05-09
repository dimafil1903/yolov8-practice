import time

import pytest
import aiohttp
import asyncio
from PIL import Image
import io


# Convert image to bytes
def image_to_bytes(image_path):
    with open(image_path, 'rb') as image_file:
        img = Image.open(image_file)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        return img_byte_arr.getvalue()


# Asynchronous function to post requests
async def post_image(session, url, image_bytes):
    start_time = time.perf_counter()
    async with session.post(url, data={'file': image_bytes}) as response:
        assert response.status == 200
        response_data = await response.json()
    end_time = time.perf_counter()
    return response_data, end_time - start_time


# Test to simulate multiple requests
@pytest.mark.asyncio
async def test_high_volume_requests():
    image_bytes = image_to_bytes('test_image.jpg')
    url = 'http://127.0.0.1:8001/img_object_detection_to_json'
    tasks = []

    async with aiohttp.ClientSession() as session:
        for _ in range(5):  # Number of requests to simulate
            task = asyncio.create_task(post_image(session, url, image_bytes))
            tasks.append(task)

        responses_and_times = await asyncio.gather(*tasks)
        total_time = sum(times for _, times in responses_and_times)
        average_time = total_time / len(responses_and_times)
        print(f'Average response time: {average_time:.2f} seconds')


# Running the test
if __name__ == "__main__":
    pytest.main()
