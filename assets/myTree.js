import React from "react";
import Tree from "react-d3-tree";

const containerStyles = {
  width: '100%',
  height: '100vh',
}

const renderRectSvgNode = ({ nodeDatum, toggleNode }) => (
    <g color={nodeDatum.attributes?.color ? nodeDatum.attributes?.color : "black"}>
      <rect x="-18" y="-18" width="36" height="25" fill="white" strokeWidth="0"></rect>
      <text fill="currentcolor" x="0" y="0" strokeWidth="0.5" stroke="currentcolor">
        {nodeDatum.name}
      </text>
    </g>
);

export class CenteredTree extends React.PureComponent {
  state = {}

resize = () => { this.setState({
      translate: {
        x: window.innerWidth / 2,
        y: 50
      }
    });
}

  componentDidMount() {
    this.setState({
      translate: {
        x: window.innerWidth / 2,
        y: 50
      }
    });
    window.addEventListener('resize', this.resize)
  }

  componentWillUnmount() {
      window.removeEventListener('resize', this.resize)
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
          renderCustomNodeElement={renderRectSvgNode}
        />
      </div>
    );
  }
}
