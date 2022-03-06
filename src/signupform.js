'use strict';

import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'
import ReactDOM from 'react-dom'
import React from 'react'
import Combobox from "react-widgets/Combobox";

import "react-widgets/styles.css";

const e = React.createElement;

class SignupButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      signup: true,
      isLoaded: false,
      emails: []
    };
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    e.preventDefault();
    if (!this.state.isLoaded) {
      fetch("/email_suggest/")
        .then(res => res.json())
        .then(
          (res) => {
            this.setState({
              isLoaded: true,
              emails: res.items
            });
          },
          // Note: it's important to handle errors here
          // instead of a catch() block so that we don't swallow
          // exceptions from actual bugs in components.
          (error) => {
            this.setState({
              isLoaded: true,
              emails: []
            });
          }
        )
        }
    this.setState({
      signup: ! this.state.signup
    })
  }

  show_available() {
    return (
      <a onClick={this.handleClick}>
        { (this.props.volunteer == null)? "Signup!": this.props.volunteer }
      </a>
    )
  }

  show_signup() {
    var user_row = ""
    if (this.props.is_coordinator === "True") {
      user_row = (
        <Row style={{ paddingBottom: '1em' }} >
        <Col sm={12}>
          User:
          <Combobox
              hideCaret
              hideEmptyPopup
              placeholder="Search for email..."
              data={this.state.emails}
          />
        </Col>
        </Row>
      )
    }
    return (
      <Container fluid={true}>
        {user_row}
        <Row style={{ paddingBottom: '1em' }} >
          <Col sm={12}>
            Comment:
            <input style={{ width: '100%' }} type="text" name="name" />
          </Col>
        </Row>
        <Row>
          <Col sm={2}><Button onClick={this.handleClick}>Submit</Button></Col>
          <Col sm={2}><Button variant='danger' onClick={this.handleClick}>Cancel</Button></Col>
        </Row>
      </Container>
    )
  }

  render() {
    if (this.state.signup) {
      return this.show_available()
    }
    else {
      return this.show_signup()
    }
  }

  componentDidMount() {
  }

}

const domContainer = document.querySelectorAll('.jobsignup');
domContainer.forEach(
  element => {
    ReactDOM.render(e(SignupButton, { 
      'candelete': element.getAttribute('candelete'),
      'job': element.getAttribute('jobid'),
      'volunteer': element.getAttribute('volunteer'),
      'is_coordinator': element.getAttribute('is_coordinator')
    }), element);
  }
)
