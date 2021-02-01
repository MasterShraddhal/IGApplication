from django.contrib.auth.base_user import BaseUserManager


class CustomManager(BaseUserManager):

    def create_user(self,email,first_name,last_name,age,username,password,profile=None):
        if not email:
            raise ValueError("Users must have email")
        if not password:
            raise ValueError("Password must be given")
        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            age=age,
            username=username,
            profile=profile
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self,email,first_name,last_name,age,username,password):
        user=self.create_user(email,first_name,last_name,age,username,password)
        user.staff=True
        user.save(using=self._db)
        return user

    def create_superuser(self,email,first_name,last_name,age,username,password=None):
        user=self.create_user(email,first_name,last_name,age,username,password)
        user.staff=True
        user.superuser=True
        user.save(using=self._db)
        return user