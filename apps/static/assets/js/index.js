
const tagContainer = document.getElementById('tag-container');
const input = document.getElementById('myInput');

let tags = [];

input.addEventListener('keyup', function(e) {
    if (e.key === 'Enter') { 
        tags.push(input.value);
        addTags(); 
        input.value = '';
    }
})

function addTags() {
    reset();
    tags.slice().reverse().forEach(function(tag) {
        const input = createTag(tag);
        tagContainer.prepend(input);
    })
}

function reset() {
    document.querySelectorAll('.tag').forEach(function(tag) {
        tag.parentElement.removeChild(tag);
    })
}

function createTag(label) {
    const div = document.createElement('div');
    div.setAttribute('class', 'tag');
    const span = document.createElement('span');
    span.innerHTML = label;
    const closeBtn = document.createElement('i');
    closeBtn.setAttribute('class', 'material-icons');
    closeBtn.setAttribute('data-item', label);
    closeBtn.innerHTML = 'x';

    div.appendChild(span);
    div.appendChild(closeBtn);
    return div;
}

document.addEventListener('click', function(e) {
    if (e.target.tagName === 'I') {
        const value = e.target.getAttribute('data-item');
        const index = tags.indexOf(value);
        tags = [...tags.slice(0, index), ...tags.slice(index + 1)];
        addTags();
    }
})

function send() {
    valid = true;
    
    if (tags.length < 1) {
        valid = false
    }
    
    tags.forEach(function(tag) {
        if (!validateEmail(tag)) {
            valid = false
        };
    })
    
    if (valid == true) {
        sendEmail();
    }
    else {
        document.getElementById('error').style.display = 'block';
        document.getElementById('success').style.display = 'none';
    }
}

/*function validateEmail(email) {
    const re = "/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)";
    return re.test(email);
}*/

function validateEmail(email) {
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))
    {
        return (true)
    }
    return (false)
}

function sendEmail() {
    document.getElementById('success').style.display = "block";
    document.getElementById('error').style.display = "none";
}