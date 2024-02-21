import React from "react";
import Tree from "react-d3-tree";

const containerStyles = {
  width: '100%',
  height: '100vh',
}

export class CenteredTree extends React.PureComponent {
  state = {}

  componentDidMount() {
    this.setState({
      translate: {
        x: window.innerWidth / 2,
        y: 50
      }
    });
  }

  render() {
    return (
      <div style={containerStyles} ref={tc => (this.treeContainer = tc)}>
        <Tree
          data={this.props.data}
          translate={this.state.translate}
          orientation={this.props.orientation}
          pathFunc={this.props.pathFunc}
          draggable={this.props.draggable}
          zoomable={this.props.zoomable}
        />
      </div>
    );
  }
}
