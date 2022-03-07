'use strict';

import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'
import ReactDOM from 'react-dom'
import React from 'react'
import Combobox from "react-widgets/Combobox";
import Cookies from 'js-cookie'

import "react-widgets/styles.css";
import { ThemeConsumer } from 'react-bootstrap/esm/ThemeProvider';

const e = React.createElement;

class SignupButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      signup: true,
      isLoaded: false,
      emails: [],
      comment: ''
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
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

  handleSubmit(e) {
    e.preventDefault();
    const csrftoken = Cookies.get('csrftoken');
    fetch('/signup/', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({
        'user': this.state.user,
        'jobid': this.props.job,
        'comment': this.state.comment 
      })
    }).then(response => {
      if (!response.ok) {
        window.confirm("There was an error signing up. Someone might have got there first or you're already busy at this time.")
      }
      location.reload()
    }).catch(error => {
      window.confirm("Something went wrong!")
      location.reload()
    })
  }

  handleDelete(e) {
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
        'signup': this.props.candelete,
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

  show_available() {
    return (
      <a onClick={this.handleClick}>
        { (this.props.volunteer == null)? "Signup!": this.props.volunteer }
      </a>
    )
  }

  show_deleteable() {
    return (
      <>
        { (this.props.volunteer == null)? "Signup!": this.props.volunteer }
        <Button variant='danger' onClick={this.handleDelete}>Delete</Button>
      </>      
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
              onChange={value => this.setState({'user': value})}
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
            <input 
              style={{ width: '100%' }} 
              type="text" 
              value={this.state.comment} 
              onChange={(event) => {this.setState({'comment': event.target.value})}} 
            />
          </Col>
        </Row>
        <Row>
          <Col sm={2}><Button onClick={this.handleSubmit}>Submit</Button></Col>
          <Col sm={2}><Button variant='danger' onClick={this.handleClick}>Cancel</Button></Col>
        </Row>
      </Container>
    )
  }

  render() {
    if (this.state.signup) {
      if (this.props.candelete === 'None') {
        return this.show_available()
      }
      else {
        return this.show_deleteable()
      }
    }
    else {
      return this.show_signup()
    }
  }
}

const domContainer = document.querySelectorAll('.jobsignup');
domContainer.forEach(
  element => {
    ReactDOM.render(e(SignupButton, { 
      'candelete': element.getAttribute('candelete'),
      'job': element.getAttribute('jobid'),
      'volunteer': element.getAttribute('volunteer'),
      'is_coordinator': element.getAttribute('is_coordinator'),
    }), element);
  }
)
