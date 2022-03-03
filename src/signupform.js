'use strict';

import Modal from './react-bootstrap/Modal'

const e = React.createElement;

class SignupButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };

    // This binding is necessary to make `this` work in the callback    
    this.handleClick = this.handleClick.bind(this);
    
  }

  handleClick(e) {
    e.preventDefault();    
    alert('You clicked submit.');
  }

  render() {
    return (
      <a onClick={this.handleClick}>Signup</a>
    )
  }
}

const domContainer = document.querySelectorAll('.jobsignup');
domContainer.forEach(
  element => {
    ReactDOM.render(e(SignupButton, { 'job': element.getAttribute('jobid')} ), element);
  }
)
