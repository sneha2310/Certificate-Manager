// function domainPage() {

//     document.getElementById("domain_inp1").hidden = true;
//     document.getElementById("domain_inp2").hidden = true;
// }

function validateForms() {

    var flag = true;

    var csrnamedns1 = document.forms["domainent"]["ipvalue"].value;
            if  (csrnamedns1){
                    // console.log("Inside")
                    if (/^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$/.test(csrnamedns1)) {
                        
                            document.getElementById("domain_inp1").hidden = true;

                        
                        } else {
                            console.log("else")
                            document.getElementById("domain_inp1").hidden = false;
                            flag = false;
                        }
                    }
    console.log(csrnamedns1)
    var csrnamedns2 = document.forms["domainent"]["fqdnvalue"].value;
            if  (csrnamedns2){
                        document.getElementById("domain_inp2").hidden = true;


                }  
    console.log(csrnamedns2)  
    if (flag) {

        return true;

    } else {

        return false;
    }
    }

