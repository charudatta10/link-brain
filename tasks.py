from invoke import task, Collection, Context


@task
def commit(ctx, message="init"):
    ctx.run("git add .")
    ctx.run(f'git commit -m "{message}"')


@task
def quit(ctx):
    print("Copyright © 2024 Charudatta")


@task
def test(ctx):
    ctx.run("python -m unittest discover -s tests")

# Create a task to run the script
@task
def gen_site(ctx):
    """
    Compile the code, activate conda environment, run the main script,
    and copy static files to the site directory.
    """
    # Activate conda environment
    with ctx.prefix('conda activate w'):
        # Run the main script
        ctx.run("python src/main.py")
        
        # Copy static files to the site directory
        ctx.run("Copy-Item -Path src/static -Destination src/site/ -Recurse -Force", pty=True)

@task(default=True)
def default(ctx):
    # Get a list of tasks
    tasks = sorted(ns.tasks.keys())
    # Display tasks and prompt user
    for i, task_name in enumerate(tasks, 1):
        print(f"{i}: {task_name}")
    choice = int(input("Enter the number of your choice: "))
    ctx.run(f"invoke {tasks[choice - 1]}")


# Create a collection of tasks
ns = Collection(
    commit,
    quit,
    gen_site,
    test,
    default,
)
