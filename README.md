# Certificate-Manager

It is a tool used to create, generate as well as manage the Digivalet certificate. It manages the expiry time of the particular certificate along with which we can also generate a report and send it to multiple users at the same time on the email.  

## Login page:

There is the login page of the Digivalet Certificate Manager. The login page is integrated with the LDAP authentication also.


![login.png](/sync/login.png)

## CSR Generation:

As the user logged-in, the user sees the CSR generation page. The user can easily generate the certificate using the CSR Generation page. 


The user enters the DNS as per requirement like das.example.digivalet.com and clicks on the add button. The certificate is generated as shown below with the certificate which will be downloaded when the user clicks on the Download CSR button.

![csrgeneration1.png](/sync/csrgeneration1.png)
![csrgeneration2.png](/sync/csrgeneration2.png)
![csrgeneration3.png](/sync/csrgeneration3.png)

## CRT Generation:

This page generates the certificate as per the user requirement. The Open CSR dropdown displays all the created certificates. The user has the access to delete the created certificate. The user can select the file from the Choose file required as per the desired created certificate and then submit. On clicking on the submit button, the user gets the zip file as per the requirement.

![crtgeneration.png](/sync/crtgenerate.png)


## Domain Inventory:

From this page, users can easily add the entry of the host as well as update the entry of the host.

![domain_inventory.png](/sync/domain_inventory.png)

We can also visualize the IP of the FQDN whose certificate is generated. 

![domaininventory2.png](/sync/domainInventory2.png)


URL Inventory:

This page gives us all the related Fqdn of the particular property. This is the collection of the properties whose certificates are generated using this tool at the same place. These tiles are the dropdowns.

![urlinventory.png](/sync/URLInventory.png)

## CERT Expiry Details:

This page tells us about the details about the expiry of the particular property if it is reachable. These tiles are the dropdowns having the expiry status of the related property. By clicking on the Refresh button, all the data like its expiry date of a particular Fqdn will be updated. 



![cert-expiry-status.png](/sync/cert-expiry-status.png)



Generate Report: 

Using this, users can generate the report of the data which will expire within 15 or 30 days as per the user requirement. Users can also send mail to multiple users at the same time.


![cert-expiry-status1.png](/sync/cert-expiry-status1.png)

Unreachable:

The user gets the list of all the Fqdn which are unreachable using this button.

![unreachable.png](/sync/unreachable.png)



## Release Notes Template

Company / Product Name : Certificate-Manager
Version: 1.2.3
Date:
    
👍 New Features
    • The software checks every day and  gets notify on the slack at a particular channel whenever the certificate expiry after 30 days.
    • The software shows all the FQDNs related to partcular servers as the drop down in the particular tiles.
    • Can generate the report and send it to multiple users it certificate expires within 30 or 15 days.

✅ Fixed Issues
    • Reduce manual work of generating and creating certificates.
    • Manages the certificate and its notifies whenever they expires.
    • Get notification on daily basis if it expires after 30 days.
    • Check the modulus of the server key and generate the accurate certificate.
    • Helps to preserve all the certificates at a particular place.
    • Helps to add and update and keep record of all the FQDNs whose certificates are generated.
       
