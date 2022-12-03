function validateFormsip() {

    var flag = true;

    var csrnamedns1 = document.forms["oldnewip"]["oldip"].value;
    console.log(csrnamedns1)
        if  (csrnamedns1){
                // console.log("Inside")
                if (/^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$/.test(csrnamedns1)) {
                    
                        document.getElementById("old_inp").hidden = true;

                    
                    } else {
                        console.log("else")
                        document.getElementById("old_inp").hidden = false;
                        flag = false;
                    }
                }

    var csrnamedns2 = document.forms["oldnewip"]["oldfqdn"].value;
            if  (csrnamedns2){
                    // console.log("Inside")
                        
                            document.getElementById("old_fqdn").hidden = true;

                    }


    var csrnamedns3 = document.forms["oldnewip"]["newinp"].value;
            if  (csrnamedns3){
                    console.log('hey'+csrnamedns3)
                    if (/^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$/.test(csrnamedns3)) {
                        
                            document.getElementById("new_inp").hidden = true;

                        
                        } else {
                            console.log("else")
                            document.getElementById("new_inp").hidden = false;
                            flag = false;
                        }
                    }
    var csrnamedns4 = document.forms["oldnewip"]["newfqdn"].value;
            if  (csrnamedns4){
                    // console.log("Inside")
                                        
                            document.getElementById("new_fqdn").hidden = true;

                    }


    if (flag) {

        return true;

    } else {

        return false;
    }
    }