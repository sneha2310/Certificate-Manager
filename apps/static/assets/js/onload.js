function loadPage()
{
    try{
        // document.getElementById("csrgen").reset();        
        document.getElementById("dns_inp1").hidden = true;
        document.getElementById("dns_inp2").hidden = true;
        document.getElementById("dns_inp3").hidden = true;
        document.getElementById("dns_inp4").hidden = true;
        document.getElementById("dns_inp5").hidden = true;
        document.getElementById("dns_inp6").hidden = true;
        document.getElementById("dns_inp7").hidden = true;
        document.getElementById("dns_inp8").hidden = true;
    } catch(err) {
        try{
        document.getElementById("domain_inp1").hidden = true;
        document.getElementById("domain_inp2").hidden = true;        
        }
        catch(err){
            try{
                document.getElementById("old_inp").hidden = true;
                document.getElementById("old_fqdn").hidden = true;
                document.getElementById("new_inp").hidden = true;
                document.getElementById("new_fqdn").hidden = true;
            }
            catch(err){
                try{
                    document.getElementById("mail_id").hidden = true; 
                    }
                    catch(err){
                        
                    }
            }           
        }
    }
}

function validateForm() {

    var flag = true;
    // console.log(document.getElementById("dns_inp8").hidden);
    // var originalvalue = document.getElementById("getValues").value;
    // document.forms.reset();
    // var csrnamedns1 = document.forms["csrgen"]["dns1"].value;
    // console.log(csrnamedns1);
    var csrnamedns1 = document.forms["csrgen"]["dns1"].value;
    if (csrnamedns1.length != ""){
                // if (/^([a-zA-Z0-9/./-/*])*$/.test(csrnamedns1)) 
                    // (.+?)(?=\.)
                // if (/((\w*\-)\:\/\/)?((([\w\-]*\.)|\*\.)?([\w\-]*))\.(\w*)(\:(\d*))?/.test(csrnamedns1))
                if (/^(?!:\/\/)([a-zA-Z0-9][a-zA-Z0-9-]+\.)?[a-zA-Z0-9][a-zA-Z0-9-]+\.[a-zA-Z]{2,6}?$/.test(csrnamedns1))

                // if (/^((?!-)[A-Za-z0-9*]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}$/.test(csrnamedns1))

                // if (/(?=^.{4,253}$)(?=^*)(^((?!-)[a-zA-Z0-9-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,63}$)/.test(csrnamedns1))
                // if (/^(?!:\/\/)(?=.{1,255}$)((.{1,63}\.){1,127}(?![0-9]*$)[a-z0-9-]+\.?)$/.test(csrnamedns1))
                {
                    console.log("Hey");
                    document.getElementById("dns_inp1").hidden = true;

                
                } else {
                    
                    document.getElementById("dns_inp1").hidden = false;
                    flag = false;
                }
            }

    var csrnamedns2 = document.forms["csrgen"]["dns2"].value;
            if (csrnamedns2.length != ""){
                    if (/((\w*\-)\:\/\/)?((([\w\-]*\.)|\*\.)?([\w\-]*))\.(\w*)(\:(\d*))?/.test(csrnamedns2)) {
                    
                        document.getElementById("dns_inp2").hidden = true;
    
                    
                    } else {
                    
                        document.getElementById("dns_inp2").hidden = false;
                        flag = false;
                    }
                }

    var csrnamedns3 = document.forms["csrgen"]["dns3"].value;
                if (csrnamedns3.length != ""){
                        if (/((\w*)\:\/\/)?((([\w\-]*\.)|\*\.)?([\w\-]*))\.(\w*)(\:(\d*))?/.test(csrnamedns3)) {
                        
                            document.getElementById("dns_inp3").hidden = true;
        
                        
                        } else {
                        
                            document.getElementById("dns_inp3").hidden = false;
                            flag = false;
                        }
                    }

    var csrnamedns4 = document.forms["csrgen"]["dns4"].value;
                    if (csrnamedns4.length != ""){
                            if (/((\w*)\:\/\/)?((([\w\-]*\.)|\*\.)?([\w\-]*))\.(\w*)(\:(\d*))?/.test(csrnamedns4)) {
                            
                                document.getElementById("dns_inp4").hidden = true;
            
                            
                            } else {
                            
                                document.getElementById("dns_inp4").hidden = false;
                                flag = false;
                            }
                        }

    var csrnamedns5 = document.forms["csrgen"]["dns5"].value;
                        if (csrnamedns5.length != ""){
                                if (/((\w*)\:\/\/)?((([\w\-]*\.)|\*\.)?([\w\-]*))\.(\w*)(\:(\d*))?/.test(csrnamedns5)) {
                                
                                    document.getElementById("dns_inp5").hidden = true;
                
                                
                                } else {
                                
                                    document.getElementById("dns_inp5").hidden = false;
                                    flag = false;
                                }
                            }
    var csrnamedns6 = document.forms["csrgen"]["dns6"].value;
                            if (csrnamedns6.length != ""){
                                    if (/((\w*)\:\/\/)?((([\w\-]*\.)|\*\.)?([\w\-]*))\.(\w*)(\:(\d*))?/.test(csrnamedns6)) {
                                    
                                        document.getElementById("dns_inp6").hidden = true;
                    
                                    
                                    } else {
                                    
                                        document.getElementById("dns_inp6").hidden = false;
                                        flag = false;
                                    }
                                }
    var csrnamedns7 = document.forms["csrgen"]["dns7"].value;
                                if (csrnamedns7.length != ""){
                                        if (/((\w*)\:\/\/)?((([\w\-]*\.)|\*\.)?([\w\-]*))\.(\w*)(\:(\d*))?/.test(csrnamedns7)) {
                                        
                                            document.getElementById("dns_inp7").hidden = true;
                        
                                        
                                        } else {
                                        
                                            document.getElementById("dns_inp7").hidden = false;
                                            flag = false;
                                        }
                                    }
    var csrnamedns8 = document.forms["csrgen"]["dns8"].value;
                                    if (csrnamedns8.length != ""){
                                            if (/((\w*)\:\/\/)?((([\w\-]*\.)|\*\.)?([\w\-]*))\.(\w*)(\:(\d*))?/.test(csrnamedns8)) {
                                            
                                                document.getElementById("dns_inp8").hidden = true;
                            
                                            
                                            } else {
                                            
                                                document.getElementById("dns_inp8").hidden = false;
                                                flag = false;
                                            }
                                        }
                                        // document.forms["csrgen"].reset();
    if (flag) {
        document.getElementById("dns_inp1").reset();
        return true;

    } else {

        return false;
    }
    }
