class CreateTouches < ActiveRecord::Migration[5.1]
  def change
    create_table :touches do |t|

      t.timestamps
    end
  end
end
