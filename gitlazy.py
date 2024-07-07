#!/opt/homebrew/bin/python3.12
import argparse
import os
from drivers import git


AI_MODEL = "gemini"

def get_ai_model():
    match AI_MODEL:
        case "gemini": 
            from models.gemini import Model
            ai_model = Model()
        case "open-ai":
            raise NotImplemented
        case "llama":
            raise NotImplemented

    return ai_model

def main(args):
    model = get_ai_model()
    driver = git.GitDriver()
    
    raw_diff = driver.get_current_diff(args.verbose)

    comment = model.generate(raw_diff, args.verbose or args.ask_before_commit, args.custom_header)
    
    if args.commit:
        driver.commit_with_comment(comment, args.ask_before_commit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='GitLazy', 
                                     description='Uses AI to generate git comments from a git diff')
    parser.add_argument('-c', '--commit', action='store_true', default=False)
    parser.add_argument('-a', '--ask-before-commit', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    parser.add_argument('-w', '--custom-header', default="")

    args = parser.parse_args()

    main(args)