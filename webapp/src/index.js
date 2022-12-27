import './index.scss';

let buttons = document.getElementById('buttons');

fetch(window.conf.deviceUrl + '/api/script/', {
  method: 'GET',
}).then((resp) => {
  resp.json().then((body) => {
    body.scripts.forEach((s) => {
      let button = document.createElement('BUTTON');
      let text = document.createTextNode(s);
      button.appendChild(text);
      buttons.appendChild(button);
      button.addEventListener('click', () => {
        runScript(s);
      })
    })
  });
});

let runScript = (scriptname) => {
  // runs the script
  fetch(window.conf.deviceUrl + '/api/script/' + scriptname, {
    method: 'PUT',
  }).then((resp) => {
    console.log('ok', resp);
  });
}

