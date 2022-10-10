from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    use_in_migrations = True

    # Due to the conflicting syntax the naming takes underscore to differentiate them
    def _create_user(self, username, first_name, last_name, email,  password, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        
        if not username:
           raise ValueError('User must have a username')
        
        if not first_name:
           raise ValueError('User must have a first name')
           
        if not last_name:
           raise ValueError('User must have a last name')
        
        email=self.normalize_email(email)
        username = username
        first_name = first_name
        last_name = last_name
        user = self.model(username=username, first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


        # Assigns the extra fields to a user, these fileds are inherited from the instance of AbstractUser class
        # imported in the models.py file
    def create_user(self,username, first_name, last_name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, first_name, last_name, email, password, **extra_fields)


    def create_superuser(self, username, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff set to True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser set to True.")
        return self._create_user( username, first_name, last_name, email, password, **extra_fields)

       
       
   