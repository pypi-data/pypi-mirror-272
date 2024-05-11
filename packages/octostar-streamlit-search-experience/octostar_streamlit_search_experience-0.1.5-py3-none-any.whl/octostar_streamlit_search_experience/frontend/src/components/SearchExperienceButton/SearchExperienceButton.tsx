import { desktopApi } from "@octostar/platform-api";
import { Entity } from "@octostar/platform-types";
import { SearchExperienceButtonProps } from "../../types";

import classes from "./SearchExperienceButton.module.css";

type Props = SearchExperienceButtonProps & {
  onSearchResult: (result: Entity[]) => void;
};

function SearchExperienceButton(props: Props) {
  const { button_text = "Search" } = props;

  const handleSearchClick = async () => {
    const result = await desktopApi().searchXperience();

    props.onSearchResult(result);
  };

  return (
    <button onClick={handleSearchClick} className={classes.search_btn}>
      {button_text}
    </button>
  );
}

export default SearchExperienceButton;
