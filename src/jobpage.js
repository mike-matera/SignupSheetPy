'use strict';

const e = React.createElement;

class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };

  }

  render() {
    return (
      <div><pre>{JSON.stringify(this.props, null, 2) }</pre></div>
    )
  }
}

const domContainer = document.querySelector('#like_button_container');
const pagedata = JSON.parse(document.getElementById('page-data').textContent);
ReactDOM.render(e(LikeButton, pagedata), domContainer);