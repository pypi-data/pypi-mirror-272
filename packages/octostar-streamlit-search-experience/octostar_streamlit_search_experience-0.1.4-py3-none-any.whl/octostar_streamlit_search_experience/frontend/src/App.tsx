import { Entity } from "@octostar/platform-types";
import { useEffect } from "react";
import {
  ComponentProps,
  Streamlit,
  withStreamlitConnection,
} from "streamlit-component-lib";
import SearchExperienceButton from "./components/SearchExperienceButton/SearchExperienceButton";
import {
  ComponentDef,
  DropzoneProps,
  ParamsHost,
  SearchExperienceButtonProps,
} from "./types";
import Dropzone from "./components/Dropzone/Dropzone";

type SearchExperienceButtonDef = ComponentDef<
  "search_experience_button",
  SearchExperienceButtonProps
>;

type DropzoneDef = ComponentDef<"dropzone", DropzoneProps>;

type ArgsType = ParamsHost<SearchExperienceButtonDef | DropzoneDef>;

function App(props: ComponentProps) {
  const args: ArgsType = props.args;

  useEffect(() => {
    Streamlit.setFrameHeight();
  }, []);

  const handleSearchResult = async (result: Entity[]) => {
    console.log("search result", result);

    Streamlit.setComponentValue(result);
    Streamlit.setFrameHeight();
  };

  const handleDropZoneResult = async (result: Entity[]) => {
    console.log("dropzone result", result);

    Streamlit.setComponentValue(result);
    Streamlit.setFrameHeight();
  };

  switch (args.params.component) {
    case "search_experience_button":
      return (
        <SearchExperienceButton
          {...args.params.props}
          onSearchResult={handleSearchResult}
        />
      );

    case "dropzone":
      return (
        <Dropzone
          {...args.params.props}
          onSearchResult={handleDropZoneResult}
          onDropResult={handleDropZoneResult}
        />
      );

    default:
      console.warn(
        `Unknown component type: ${
          (args.params as { component: string }).component
        }`
      );
      return null;
  }
}

const ConnectedApp = withStreamlitConnection(App);

ConnectedApp.displayName = "SearchExperience";

export default ConnectedApp;
