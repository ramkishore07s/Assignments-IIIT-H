class AddTouchesToSingleChoices < ActiveRecord::Migration[5.1]
  def change
    add_reference :single_choices, :touch, foreign_key: true
  end
end
