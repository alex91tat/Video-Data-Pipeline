from orchestrator import Orchestrator

def main():
    file_path = "Video.mp4"
    output_path = "movie_101"

    orchestrator = Orchestrator(file_path, output_path)
    orchestrator.run()

if __name__ == "__main__":
    main()