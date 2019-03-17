class CreateSingleChoices < ActiveRecord::Migration[5.1]
  def change
    create_table :single_choices do |t|
      t.string :answer

      t.timestamps
    end
  end
end
