Express Mpesa Integration
=========================

An app that integrates Mpesa Express into Django.

**Quick start**
---------------

1. Add "express" to your INSTALLED_APPS setting like this::

       INSTALLED_APPS = [
           "express",
       ]

2. Update the config settings for Mpesa:

   ::

       # Mpesa configurations
       MPESA_CONSUMER_SECRET=
       MPESA_ACCESS_TOKEN_URL=
       MPESA_CONSUMER_KEY=
       MPESA_SHORT_CODE=
       MPESA_STK_PUSH_URL=
       MPESA_API_KEY=
       MPESA_CALLBACK_URL=
       BASE_URL=

3. Include the express URLs in your project's URLs like this::

       url(r'^express/', include('express.urls')),

4. Run the following command to create the express models:

   ::

       python manage.py migrate

5. Start the development server and visit http://127.0.0.1:8000 to use the endpoints::

       express/checkout

