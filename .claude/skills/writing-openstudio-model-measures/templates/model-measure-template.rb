# frozen_string_literal: true

# Start the measure
class YourMeasureName < OpenStudio::Measure::ModelMeasure
  # Human-readable name
  def name
    # Measure name should be the title case of the class name.
    return 'Your Measure Name'
  end

  # Human-readable description
  def description
    return 'Replace this text with an explanation of what the measure does in terms that can be understood by a general building professional audience (building owners, architects, engineers, contractors, etc.). This description will be used to create reports aimed at convincing the owner and/or design team to implement the measure in the actual building design. For this reason, the description may include details about how the measure would be implemented, along with explanations of qualitative benefits associated with the measure. It is good practice to include citations in the measure if the description is taken from a known source or if specific benefits are listed.'
  end

  # Human-readable description of modeling approach
  def modeler_description
    return 'Replace this text with an explanation for the energy modeler specifically. It should explain how the measure is modeled, including any requirements about how the baseline model must be set up, major assumptions, citations of references to applicable modeling resources, etc. The energy modeler should be able to read this description and understand what changes the measure is making to the model and why these changes are being made. Because the Modeler Description is written for an expert audience, using common abbreviations for brevity is good practice.'
  end

  # Define the arguments that the user will input
  def arguments(model)
    args = OpenStudio::Measure::OSArgumentVector.new

    # Example: Double argument
    # example_double = OpenStudio::Measure::OSArgument.makeDoubleArgument('example_double', true)
    # example_double.setDisplayName('Example Double Argument')
    # example_double.setDescription('This is an example double argument with units.')
    # example_double.setUnits('ft')
    # example_double.setDefaultValue(10.0)
    # args << example_double

    # Example: Integer argument
    # example_integer = OpenStudio::Measure::OSArgument.makeIntegerArgument('example_integer', true)
    # example_integer.setDisplayName('Example Integer Argument')
    # example_integer.setDescription('This is an example integer argument.')
    # example_integer.setDefaultValue(5)
    # args << example_integer

    # Example: Boolean argument
    # example_bool = OpenStudio::Measure::OSArgument.makeBoolArgument('example_bool', true)
    # example_bool.setDisplayName('Example Boolean Argument')
    # example_bool.setDescription('This is an example boolean argument.')
    # example_bool.setDefaultValue(true)
    # args << example_bool

    # Example: Choice argument
    # choices = OpenStudio::StringVector.new
    # choices << 'Option 1'
    # choices << 'Option 2'
    # choices << 'Option 3'
    # example_choice = OpenStudio::Measure::OSArgument.makeChoiceArgument('example_choice', choices, true)
    # example_choice.setDisplayName('Example Choice Argument')
    # example_choice.setDescription('This is an example choice argument.')
    # example_choice.setDefaultValue('Option 1')
    # args << example_choice

    # Example: String argument
    # example_string = OpenStudio::Measure::OSArgument.makeStringArgument('example_string', true)
    # example_string.setDisplayName('Example String Argument')
    # example_string.setDescription('This is an example string argument.')
    # example_string.setDefaultValue('default_value')
    # args << example_string

    return args
  end

  # Define what happens when the measure is run
  def run(model, runner, user_arguments)
    super(model, runner, user_arguments)

    # Use the built-in error checking
    if !runner.validateUserArguments(arguments(model), user_arguments)
      return false
    end

    # Assign the user inputs to variables
    # example_double = runner.getDoubleArgumentValue('example_double', user_arguments)
    # example_integer = runner.getIntegerArgumentValue('example_integer', user_arguments)
    # example_bool = runner.getBoolArgumentValue('example_bool', user_arguments)
    # example_choice = runner.getStringArgumentValue('example_choice', user_arguments)
    # example_string = runner.getStringArgumentValue('example_string', user_arguments)

    # Check the argument values for reasonableness
    # if example_double < 0
    #   runner.registerError('Example double argument must be greater than or equal to 0.')
    #   return false
    # end

    # Report initial condition of model
    # runner.registerInitialCondition("The building started with #{model.getSpaces.size} spaces.")

    # Add your measure logic here
    # Example: Iterate through spaces
    # model.getSpaces.each do |space|
    #   runner.registerInfo("Processing space: #{space.name}")
    #
    #   # Check for optional properties safely
    #   if space.thermalZone.is_initialized
    #     zone = space.thermalZone.get
    #     runner.registerInfo("  Space is in thermal zone: #{zone.name}")
    #   else
    #     runner.registerWarning("  Space '#{space.name}' is not assigned to a thermal zone.")
    #   end
    # end

    # Example: Handle "not applicable" case
    # if some_condition_that_means_measure_doesnt_apply
    #   runner.registerAsNotApplicable('This measure is not applicable because...')
    #   return true
    # end

    # Report final condition of model
    # runner.registerFinalCondition("The building finished with #{model.getSpaces.size} spaces.")

    return true
  end
end

# Register the measure to be used by the application
YourMeasureName.new.registerWithApplication
