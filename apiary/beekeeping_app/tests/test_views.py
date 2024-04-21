from django.test import TestCase
from django.urls import reverse
from beekeeping_app.models import Apiary, Keeper
from beekeeping_app.forms import HiveForm, ApiaryForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from beekeeping_app.models import Apiary, Keeper
from django.contrib.auth.models import User

class ApiaryDetailViewTest(TestCase):
    def setUp(self):
        #create a sample Apiary
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.apiary = Apiary.objects.create(title='Test Apiary', contact_email='test@example.com')

    def test_apiary_detail_view(self):
        """Test Apiary detail view"""
        #check if the correct details are listed in the detail view for this Apiary
        url = reverse('apiary-detail', args=[self.apiary.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Apiary')
        self.assertContains(response, 'test@example.com')

class UpdateApiaryViewTest(TestCase):
    def setUp(self):
        #create a sample Apiary (include keeper so we can check authentication)
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.apiary = Apiary.objects.create(title='Test Apiary', contact_email='test@example.com')
        self.keeper = Keeper.objects.create(user=self.user, apiary=self.apiary)

    def test_update_apiary_view_logged_in(self):
        """Test Update Apiary view when user is logged in"""
        #login as testuser
        self.client.login(username='testuser', password='12345')

        #access the update apiary view
        url = reverse('update-apiary', args=[self.keeper.id, self.apiary.id])
        response = self.client.get(url)

        #verify that the response status code is 200 (allowed to access the update-apiary page)
        self.assertEqual(response.status_code, 200)

    def test_update_apiary_view_not_logged_in(self):
        """Test Update Apiary view when user is not logged in"""
        #access the update apiary view without logging in
        url = reverse('update-apiary', args=[self.keeper.id, self.apiary.id])
        response = self.client.get(url)

        #verify that the response status code is 302 (not allowed to access the update-apiary page)
        self.assertEqual(response.status_code, 302)


'''
FOR CONTEXT:

updateApiary urls.py:
path('keeper/<int:keeper>/update-apiary/<int:apiary>/', views.updateApiary, name='update-apiary'),

updateApiary views.py:
@login_required(login_url='login')
@allowed_users(allowed_roles=['beekeeper_role'])
def updateApiary(request, keeper, apiary):
    apiary_instance = Apiary.objects.get(id=apiary)
    if apiary_instance.keeper.user != request.user:
        raise PermissionDenied("You don't have permission to edit this apiary.")
    
    if request.method == "POST":
        form = ApiaryForm(request.POST, request.FILES, instance=apiary_instance)
        if form.is_valid():
            image = request.FILES.get('company_logo')
            if image:
                # Open the image using PIL
                img = Image.open(image)
                # Convert RGBA to RGB
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                # Resize the image to the desired dimensions (e.g., 300x300)
                img.thumbnail((40, 40))
                # Save the resized image to a BytesIO buffer
                output = BytesIO()
                img.save(output, format='JPEG')
                # Save the resized image to the FileField
                apiary_instance.company_logo.save(image.name, output)
            form.save()
            return redirect('apiary-detail', apiary_instance.id) 
    else:
        form = ApiaryForm(instance=apiary_instance)

    return render(request, 'beekeeping_app/update_apiary.html', {'apiary': apiary_instance, 'form': form})
'''