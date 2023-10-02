import react, { useState } from "react";
import axios from "axios";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import { Grid, TextareaAutosize } from "@mui/material";
import { Button } from "@mui/material";


const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: "center",
  color: theme.palette.text.secondary,
  margin: theme.spacing(1),
}));

enum Ans {
  A = "A",
  B = "B",
  C = "C",
  D = "D",
}


interface IAns {
  answer: string;
  explain: string;
}

interface IQuiz {
  question: string;
  a: string;
  b: string;
  c: string;
  d: string;
}

function App() {

  const [loadingGenQuiz, setLoadingGenQuiz] = useState(false);
  const [isQuiz, setIsQuiz] = useState(false);
  const [textareaValue, setTextareaValue] = useState('');
  const [userAns, setUserAns] = useState<Ans>();


  //ไว้โชว์เฉลย
  const [ans, setAns] = useState<IAns>({ answer: "", explain: "" });


  const handleTextareaChange = (event: { target: { value: react.SetStateAction<string>; }; }) => {
    setTextareaValue(event.target.value);
  };

  const [quiz, setQuiz] = useState<IQuiz>({
    question: "",
    a: "",
    b: "",
    c: "",
    d: "",
  });

  const genQuiz = async () => {
    try {
      setLoadingGenQuiz(true)
      setIsQuiz(true)
      setUserAns(undefined)
      const response = await axios.post('https://8nxoko13y2.execute-api.ap-southeast-1.amazonaws.com/dev/', textareaValue);
      const jsonData = await response.data;

      setQuiz({
        question: jsonData.question,
        a: ("A: " + jsonData.a),
        b: ("B: " + jsonData.b),
        c: ("C: " + jsonData.c),
        d: ("D: " + jsonData.d),
      });

      setAns({
        answer: (jsonData.answer),
        explain: (jsonData.explain),
      })
      setLoadingGenQuiz(false)
    } catch (error) { }
  };

  const onButtonClick = (value: Ans) => {
    setUserAns(value)
  }

  const buttons: JSX.Element[] = Object.values(Ans).map((value: Ans, index: number) => {
    return (
      <Grid item xs={3} sx={{ padding: "1%" }} key={index}>
        <Button variant="outlined" disabled={!isQuiz || loadingGenQuiz || !!userAns} onClick={() => onButtonClick(value)} fullWidth >
          {value}
        </Button>
      </Grid>
    );
  });

  return (
    <div style={{ height: "100%" }}>
      <Grid container spacing={2} direction={"column"} >

        <Grid item xs={12}  >
          <Item>
            <h1>GPT TRAINING beta</h1>
          </Item>
        </Grid>

        <Grid item xs={12} >
          <Box component={Item} sx={{ padding: "10px" }}>
            <TextareaAutosize
              minRows={10}
              maxRows={10}
              aria-label="textarea"
              placeholder="Enter your text here..."
              onChange={handleTextareaChange}
              style={{
                width: '98%',
                padding: "10px 1%",
                margin: 0,
                resize: 'none',
                overflow: 'auto',
              }}
            />
            <Button variant="outlined" disabled={loadingGenQuiz} onClick={genQuiz} sx={{ width: "100%" }} >
              generate question
            </Button>
          </Box>
        </Grid>

        <Grid item xs={12}>
          <Box component={Item} sx={{ height: "100%", overflow: "auto" }}>
            <Grid container
              direction="column"
              justifyContent="center"
              alignItems="center"
              sx={{ width: "100%", height: "100%" }}>
              <Grid item xs={12} >

                <Grid item xs={12} justifyContent="flex-start" >
                  <p>{quiz.question}</p>
                  <p>{quiz.a}</p>
                  <p>{quiz.b}</p>
                  <p>{quiz.c}</p>
                  <p>{quiz.d}</p>
                </Grid>

              </Grid>
            </Grid>

            <Grid item xs={12} container justifyContent={"center"} >
              <Grid container sx={{ margin: "16px" }}>
                {buttons}
              </Grid>
            </Grid>
          </Box>

        </Grid>

        <Grid item xs={12} sx={{ marginTop: "32px" }}>
          <Grid item>
            {userAns &&
              <Item>
                <h3>{ans.answer === userAns ? "Correct!" : "Wrong"} </h3>
                <p>Answer: {ans.answer}</p>
                <p>Explanation: {ans.explain}</p>
              </Item>
            }
          </Grid>
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
