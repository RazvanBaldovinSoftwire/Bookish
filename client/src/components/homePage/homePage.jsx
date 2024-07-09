import React, { Component } from "react";
import {
  HomeDiv,
  HomeTitleTag,
  HomeTitleContainer,
} from "./HomeComponents";

export class HomePage extends Component {
  render() {
    return (
        <HomeDiv>
          <HomeTitleContainer>
            <HomeTitleTag>Status:</HomeTitleTag>
            <li>{this.props.okStatus}!</li>
          </HomeTitleContainer>
        </HomeDiv>
    );
  }
}
