from django.contrib.auth.base_user import BaseUserManager



class CustomizeUser(BaseUserManager):

    def create_user(self, email, password, **kwargs):

        if not email:
            raise ValueError("Provide Email")
        email = self.normalize_email(email)

        user = self.model(email = email, **kwargs)
        user.set_password(password)
        user.is_active = True
        user.save()

        return user
    
    def create_superuser(self, email, password, **kwargs):

        
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
    

        if kwargs.get('is_staff') is not True:
            raise ValueError("User Must be Staff")
        if kwargs.get('is_superuser') is not True:
            raise ValueError("User Must be Super User")
        if kwargs.get('is_active') is not True:
            raise ValueError("User Must be active")
        
        return self.create_user(email,password, **kwargs)
