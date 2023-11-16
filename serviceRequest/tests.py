from rest_framework.test import APITestCase
from rest_framework import status
from .models import Location, ServiceRequest, RequestStatus, ServiceRequestChatMessage
from appUsers.models import CustomUser


class LocationsTests(APITestCase):
    def setUp(self):
        self.baseUrl = "/api/locations/"
        self.userData = {"username": "testUser", "password": "12345678", "is_active": True, "is_superuser": True,
                         "is_staff": True}
        self.client.post('/api/users/user-registration/', self.userData, format="json")
        response = self.client.post('/api/token/', self.userData, format="json")
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_user_can_not_get_data_without_admin_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'wrong_credentials')
        response = self.client.get('/api/locations/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_location(self):
        response = self.client.post('/api/locations/', {"location": "Location 1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_locations(self):
        self.client.post('/api/locations/', {"location": "Location 1"}, format="json")
        self.client.post('/api/locations/', {"location": "Location 2"}, format="json")
        self.client.post('/api/locations/', {"location": "Location 3"}, format="json")
        response = self.client.get('/api/locations/?location__icontains=Location 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_location(self):
        self.client.post('/api/locations/', {"location": "Location 1"}, format="json")
        location = Location.objects.get(location="Location 1")
        response = self.client.put('/api/locations/' + str(location.id) + '/', {"location": "Updated location"},
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_location(self):
        self.client.post('/api/locations/', {"location": "Location 1"}, format="json")
        location = Location.objects.get(location="Location 1")
        response = self.client.delete('/api/locations/' + str(location.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RequestStatusTests(APITestCase):
    def setUp(self):
        self.baseUrl = "/api/statuses/"
        self.userData = {"username": "testUser", "password": "12345678", "is_active": True, "is_superuser": True,
                         "is_staff": True}
        self.client.post('/api/users/user-registration/', self.userData, format="json")
        response = self.client.post('/api/token/', self.userData, format="json")
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_user_can_not_get_data_without_admin_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'wrong_credentials')
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_status(self):
        response = self.client.post(self.baseUrl, {"status": "Status 1", "status_color": "#ffff"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_statuses(self):
        self.client.post(self.baseUrl, {"status": "Status 1", "status_color": "#ffff"}, format="json")
        self.client.post(self.baseUrl, {"status": "Status 2", "status_color": "#ffff"}, format="json")
        self.client.post(self.baseUrl, {"status": "Status 3", "status_color": "#ffff"}, format="json")
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_update_status(self):
        self.client.post(self.baseUrl, {"status": "Status 1", "status_color": "#ffff"}, format="json")
        location = RequestStatus.objects.get(status="Status 1")
        response = self.client.put(self.baseUrl + str(location.id) + '/', {"status": "Status 2", "status_color": "#88ffff"},
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_status(self):
        self.client.post(self.baseUrl, {"status": "Status 1", "status_color": "#ffff"}, format="json")
        location = RequestStatus.objects.get(status="Status 1")
        response = self.client.delete(self.baseUrl + str(location.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ServiceRequestTests(APITestCase):
    def setUp(self):
        self.baseUrl = "/api/service-requests/"
        self.userData = {"username": "testUser", "password": "12345678", "is_active": True, "is_superuser": True,
                         "is_staff": True}
        self.client.post('/api/users/user-registration/', self.userData, format="json")
        response = self.client.post('/api/token/', self.userData, format="json")
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_user_can_not_get_data_without_admin_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'wrong_credentials')
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_service_requests(self):
        user = CustomUser.objects.get(username = 'testUser')
        location = Location.objects.create(location = "Location 777")
        status_ = RequestStatus.objects.create(status = "Test status")

        response = self.client.post(self.baseUrl, {"request_sender": user.id, "location": location.id, "address": "address", "request_description": "Description", "request_status": status_.id }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_service_requests(self):
        user = CustomUser.objects.get(username = 'testUser')
        location = Location.objects.create(location = "Location 777")
        status_ = RequestStatus.objects.create(status = "Test status")
        self.client.post(self.baseUrl, {"request_sender": user.id, "location": location.id, "address": "address1", "request_description": "Description1", "request_status": status_.id }, format="json")
        self.client.post(self.baseUrl, {"request_sender": user.id, "location": location.id, "address": "address2", "request_description": "Description2", "request_status": status_.id }, format="json")
        self.client.post(self.baseUrl, {"request_sender": user.id, "location": location.id, "address": "address3", "request_description": "Description3", "request_status": status_.id }, format="json")
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_update_service_requests(self):
        user = CustomUser.objects.get(username = 'testUser')
        location = Location.objects.create(location = "Location 777")
        status_ = RequestStatus.objects.create(status = "Test status")
        self.client.post(self.baseUrl, {"request_sender": user.id, "location": location.id, "address": "address1", "request_description": "Description1", "request_status": status_.id }, format="json")
        service_request = ServiceRequest.objects.get(address="address1")
        response = self.client.put(self.baseUrl + str(service_request.id) + '/', {"request_sender": user.id, "location": location.id, "address": "address33", "request_description": "Description3", "request_status": status_.id },
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_service_requests(self):
        user = CustomUser.objects.get(username = 'testUser')
        location = Location.objects.create(location = "Location 777")
        status_ = RequestStatus.objects.create(status = "Test status")
        self.client.post(self.baseUrl, {"request_sender": user.id, "location": location.id, "address": "address1", "request_description": "Description1", "request_status": status_.id }, format="json")
        service_request = ServiceRequest.objects.get(address="address1")
        response = self.client.delete(self.baseUrl + str(service_request.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ServiceRequestChatMessageTests(APITestCase):
    def setUp(self):
        self.baseUrl = "/api/messages/"
        self.userData = {"username": "testUser", "password": "12345678", "is_active": True, "is_superuser": True,
                         "is_staff": True}
        self.client.post('/api/users/user-registration/', self.userData, format="json")
        response = self.client.post('/api/token/', self.userData, format="json")
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_user_can_not_get_data_without_admin_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'wrong_credentials')
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_service_requests_message(self):
        user = CustomUser.objects.get(username = 'testUser')
        location = Location.objects.create(location = "Location 777")
        status_ = RequestStatus.objects.create(status = "Test status")
        service_request = ServiceRequest.objects.create(request_sender=user, location=location, request_status=status_, request_description="Description")        
        response = self.client.post(self.baseUrl, {"message_text": "message 1", "service_request": service_request.id, "sender": user.id }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_service_requests_message(self):
        user = CustomUser.objects.get(username = 'testUser')
        location = Location.objects.create(location = "Location 777")
        status_ = RequestStatus.objects.create(status = "Test status")
        service_request = ServiceRequest.objects.create(request_sender=user, location=location, request_status=status_, request_description="Description") 
        self.client.post(self.baseUrl, {"message_text": "message 1", "service_request": service_request.id, "sender": user.id }, format="json")
        self.client.post(self.baseUrl, {"message_text": "message 2", "service_request": service_request.id, "sender": user.id }, format="json")
        self.client.post(self.baseUrl, {"message_text": "message 3", "service_request": service_request.id, "sender": user.id }, format="json")
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_update_service_requests_message(self):
        user = CustomUser.objects.get(username = 'testUser')
        location = Location.objects.create(location = "Location 777")
        status_ = RequestStatus.objects.create(status = "Test status")
        service_request = ServiceRequest.objects.create(request_sender=user, location=location, request_status=status_, request_description="Description") 
        self.client.post(self.baseUrl, {"message_text": "message 1", "service_request": service_request.id, "sender": user.id }, format="json")
        service_request_message = ServiceRequestChatMessage.objects.get(message_text="message 1")
        response = self.client.put(self.baseUrl + str(service_request_message.id) + '/', {"message_text": "message 2", "service_request": service_request.id, "sender": user.id },
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_service_requests_message(self):
        user = CustomUser.objects.get(username = 'testUser')
        location = Location.objects.create(location = "Location 777")
        status_ = RequestStatus.objects.create(status = "Test status")
        service_request = ServiceRequest.objects.create(request_sender=user, location=location, request_status=status_, request_description="Description") 
        self.client.post(self.baseUrl, {"message_text": "message 1", "service_request": service_request.id, "sender": user.id }, format="json")
        service_request_message = ServiceRequestChatMessage.objects.get(message_text="message 1")
        response = self.client.delete(self.baseUrl + str(service_request_message.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)