export type None = null;

export type SearchExperienceButtonProps = {
  button_text: string | None;
};

export type DropzoneProps = {
  id: string;
  label: string;
};

export type ParamsHost<T> = {
  params: T;
};

export type ComponentDef<T extends string, P> = {
  component: T;
  props: P;
};
