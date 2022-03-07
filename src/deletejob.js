
import Cookies from 'js-cookie'
import Button from 'react-bootstrap/Button'
import React from 'react'
import ReactDOM from 'react-dom'

const e = React.createElement;

class DeleteButton extends React.Component {

    constructor(props) {
        super(props);
        this.do_delete = this.do_delete.bind(this);
    }
    
    do_delete(e) {
        e.preventDefault();
        if (! window.confirm("Are you sure?")) {
            return 
        }
        const csrftoken = Cookies.get('csrftoken');
        fetch('/delete/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'signup': this.props.signupid,
        })
        }).then(response => {
        if (!response.ok) {
            window.confirm("There was an error.")
        }
        location.reload()
        }).catch(error => {
        window.confirm("Something went wrong!")
        location.reload()
        })
    }

    render() {
        return <Button variant='danger' onClick={this.do_delete}>Delete</Button>
    }
}

const domContainer = document.querySelectorAll('.deletebutton');
domContainer.forEach(
  element => {
    ReactDOM.render(e(DeleteButton, { 
      'signupid': element.getAttribute('signupid'),
    }), element);
  }
)

export default DeleteButton;

