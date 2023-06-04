import React, { useState, useMemo, forwardRef } from "react";
import styled, { css } from "styled-components";
import Uploady, {
  useBatchAddListener,
  useBatchFinishListener,
  useUploady
} from "@rpldy/uploady";
import { asUploadButton } from "@rpldy/upload-button";
import 'antd/dist/antd.css';
import "./styles.css";


const inputCss = css`
  width: 260px;
  height: 30px;
  line-height: 30px;
  font-size: 22px;
  color: #000;
  border: 1px solid #fff;
  background-color: #f1f1f1;
  margin-bottom: 10px;
  box-sizing: border-box;
  padding: 0 4px;
`;

const selectCss = css`
  width: 100px;
  height: 30px;
  line-height: 30px;
  font-size: 22px;
  color: #000;
  border: 1px solid #fff;
  background-color: #f1f1f1;
  margin-bottom: 10px;
  box-sizing: border-box;
  padding: 0 4px;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;

  select[type="text"]{
    ${selectCss}
  }
`;

const SubmitButton = styled.button`
  height: 60px;
  width: 260px;
  font-size: 22px;
  margin-top: 20px;
  background-color: #101a2c;
  border: 1px solid #4b5763;
  color: #b0b1b3;
  text-transform: uppercase;
  cursor: pointer;
  margin-bottom: 4px;

  ${({ disabled }) =>
    disabled
      ? `
    cursor: default;
    background-color: #d8d2d2;
    color: #444040
  `
      : ""}
`;

const UploadField = styled.div`
  ${inputCss}

  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;

  cursor: pointer;
`;

const MyUploadField = asUploadButton(
  forwardRef(({ onChange, ...props }, ref) => {
    const [text, setText] = useState("Select file");

    useBatchAddListener((batch) => {
      setText(batch.items[0].file.name);
      onChange(batch.items[0].file.name);
    });

    useBatchFinishListener(() => {
      setText("Select file");
      onChange(null);
    });

    return (
      <UploadField {...props} ref={ref} id="form-upload-button" title={text}>
        {text}
      </UploadField>
    );
  })
);

const MyForm = () => {

  const [value, setValue] = useState();
  const [fileName, setFileName] = useState(null);
  const { processPending } = useUploady();

  const onSubmit = () => processPending({ params: value });

  const onFieldChange = (e) => {
    setValue({
      ...value,
      [e.currentTarget.id]: e.currentTarget.value
    });
  };

  const buttonExtraProps = useMemo(
    () => ({
      onChange: setFileName
    }),
    [setFileName]
  );

  return (
    <Form>
      <MyUploadField autoUpload={false} extraProps={buttonExtraProps} />

      <p>{`Please select a destination folder:`}</p>
      <select  onChange={onFieldChange}
        id="path"
        type="text"
        placeholder="upload to...">
            <option label=""></option>
            <option value="BAM">BAM</option>
            <option value="EAH">EAH</option>
            <option value="IKTS">IKTS</option>
      </select>

      <SubmitButton
        id="form-submit"
        type="button"
        onClick={onSubmit}
        disabled={!fileName}
      >
        Submit Form
      </SubmitButton>
    </Form>
  );
};

export default function App() {
  return (
    <div className="App">
      <Uploady
        clearPendingOnAdd
        destination={{ url: "/upload/" }}
        multiple={false}
      >
        <MyForm />
      </Uploady>
    </div>
  );
}
