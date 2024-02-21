import React from "react";
import Tree from "react-d3-tree";


const debugData = [
  {
    name: "1",
    children: [
      {
        name: "2"
      },
      {
        name: "2"
      }
    ]
  }
];

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
          data={debugData}
          translate={this.state.translate}
          orientation={'vertical'}
        />
      </div>
    );
  }
}
